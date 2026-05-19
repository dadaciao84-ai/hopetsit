// v23.1.148 — Daniel : "regler adresse auto ds modifier animal". Champ
// d'adresse avec autocomplétion via Nominatim (OpenStreetMap, gratuit,
// déjà utilisé par CityLocationPicker pour la ville). Cible : les
// adresses vétérinaires de la fiche pet (régulier + urgence).
//
// Différence avec CityLocationPicker :
//   - Recherche d'adresse complète (rue + ville), pas seulement la ville
//   - UI plus compacte : pas de bouton "auto-detect" ni "carte"
//   - S'intègre comme un simple TextField pour drop-in replacement.

import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'package:hopetsit/utils/app_colors.dart';
import 'package:hopetsit/widgets/app_text.dart';

class AddressAutocompleteField extends StatefulWidget {
  const AddressAutocompleteField({
    super.key,
    required this.controller,
    required this.label,
    this.onAddressSelected,
    this.maxLines = 1,
  });

  final TextEditingController controller;
  final String label;

  /// Optional callback when a suggestion is picked. Provides the full
  /// display name + lat/lon if the caller wants to save coordinates.
  final void Function(String address, double lat, double lon)? onAddressSelected;

  final int maxLines;

  @override
  State<AddressAutocompleteField> createState() =>
      _AddressAutocompleteFieldState();
}

class _AddressAutocompleteFieldState extends State<AddressAutocompleteField> {
  Timer? _debounce;
  List<_AddressSuggestion> _suggestions = const [];
  bool _loading = false;
  bool _suppressNext = false;
  String _lastQuery = '';

  @override
  void initState() {
    super.initState();
    widget.controller.addListener(_onTextChanged);
  }

  @override
  void dispose() {
    widget.controller.removeListener(_onTextChanged);
    _debounce?.cancel();
    super.dispose();
  }

  void _onTextChanged() {
    if (_suppressNext) {
      _suppressNext = false;
      return;
    }
    final q = widget.controller.text.trim();
    if (q.length < 3) {
      if (_suggestions.isNotEmpty || _loading) {
        setState(() {
          _suggestions = const [];
          _loading = false;
        });
      }
      return;
    }
    if (q == _lastQuery) return;
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 400), () => _search(q));
  }

  Future<void> _search(String q) async {
    _lastQuery = q;
    if (!mounted) return;
    setState(() => _loading = true);
    try {
      final uri = Uri.parse(
        'https://nominatim.openstreetmap.org/search'
        '?q=${Uri.encodeQueryComponent(q)}'
        '&format=json'
        '&addressdetails=1'
        '&limit=6'
        '&accept-language=${Get.locale?.languageCode ?? 'fr'}',
      );
      final res = await http.get(
        uri,
        headers: {
          'User-Agent': 'HoPetSit/23.1 (contact@hopetsit.com)',
          'Accept': 'application/json',
        },
      ).timeout(const Duration(seconds: 6));
      if (res.statusCode != 200) {
        if (!mounted) return;
        setState(() {
          _loading = false;
          _suggestions = const [];
        });
        return;
      }
      final List<dynamic> raw = json.decode(res.body);
      final List<_AddressSuggestion> out = [];
      for (final item in raw) {
        if (item is! Map) continue;
        final display = (item['display_name'] ?? '').toString();
        if (display.isEmpty) continue;
        out.add(_AddressSuggestion(
          displayName: display,
          lat: double.tryParse('${item['lat']}') ?? 0.0,
          lon: double.tryParse('${item['lon']}') ?? 0.0,
        ));
        if (out.length >= 5) break;
      }
      if (!mounted) return;
      setState(() {
        _suggestions = out;
        _loading = false;
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _loading = false;
        _suggestions = const [];
      });
    }
  }

  void _pickSuggestion(_AddressSuggestion s) {
    _suppressNext = true;
    widget.controller.text = s.displayName;
    widget.controller.selection = TextSelection.fromPosition(
      TextPosition(offset: s.displayName.length),
    );
    widget.onAddressSelected?.call(s.displayName, s.lat, s.lon);
    FocusScope.of(context).unfocus();
    setState(() {
      _suggestions = const [];
      _lastQuery = s.displayName;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextField(
          controller: widget.controller,
          maxLines: widget.maxLines,
          textInputAction: TextInputAction.search,
          decoration: InputDecoration(
            labelText: widget.label,
            border: const OutlineInputBorder(),
            suffixIcon: _loading
                ? Padding(
                    padding: EdgeInsets.all(12.w),
                    child: SizedBox(
                      width: 16.w,
                      height: 16.h,
                      child: CircularProgressIndicator(
                        strokeWidth: 1.5,
                        valueColor: AlwaysStoppedAnimation<Color>(
                          AppColors.primaryColor,
                        ),
                      ),
                    ),
                  )
                : const Icon(Icons.search),
          ),
        ),
        if (_suggestions.isNotEmpty) ...[
          SizedBox(height: 6.h),
          Container(
            decoration: BoxDecoration(
              color: AppColors.card(context),
              borderRadius: BorderRadius.circular(12.r),
              border: Border.all(color: AppColors.grey300Color, width: 1),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.06),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Column(
              children: _suggestions.map((s) {
                final last = s == _suggestions.last;
                return InkWell(
                  onTap: () => _pickSuggestion(s),
                  child: Container(
                    padding: EdgeInsets.symmetric(
                      horizontal: 12.w,
                      vertical: 10.h,
                    ),
                    decoration: BoxDecoration(
                      border: last
                          ? null
                          : Border(
                              bottom: BorderSide(
                                color: AppColors.grey300Color
                                    .withValues(alpha: 0.5),
                                width: 1,
                              ),
                            ),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          Icons.location_on_outlined,
                          color: AppColors.primaryColor,
                          size: 18.sp,
                        ),
                        SizedBox(width: 10.w),
                        Expanded(
                          child: InterText(
                            text: s.displayName,
                            fontSize: 13.sp,
                            fontWeight: FontWeight.w500,
                            color: AppColors.textPrimary(context),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
        ],
      ],
    );
  }
}

class _AddressSuggestion {
  const _AddressSuggestion({
    required this.displayName,
    required this.lat,
    required this.lon,
  });

  final String displayName;
  final double lat;
  final double lon;

  @override
  bool operator ==(Object other) =>
      other is _AddressSuggestion && other.displayName == displayName;

  @override
  int get hashCode => displayName.hashCode;
}
