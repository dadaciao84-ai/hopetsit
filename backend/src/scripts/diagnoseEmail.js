#!/usr/bin/env node
/* eslint-disable no-console */

/**
 * Diagnostic d'un email : cherche dans Owner, Sitter, Walker et affiche
 * l'état (verified, status, createdAt). Optionnel: --delete pour supprimer
 * tous les comptes fantômes (verified=false) pour cet email.
 *
 * Usage (depuis Render shell ou local avec .env) :
 *   node src/scripts/diagnoseEmail.js bodydesignpedreguer@gmail.com
 *   node src/scripts/diagnoseEmail.js bodydesignpedreguer@gmail.com --delete
 *
 * v23.1.147 — Daniel : "erreur d'inscription email déjà utilisé alors
 * que pas du tout en DB". Très probablement un compte non-vérifié qui
 * traîne d'une précédente tentative.
 */

require('dotenv').config();
const mongoose = require('mongoose');

const Owner = require('../models/Owner');
const Sitter = require('../models/Sitter');
const Walker = require('../models/Walker');

async function main() {
  const args = process.argv.slice(2);
  const email = (args[0] || '').toLowerCase().trim();
  const shouldDelete = args.includes('--delete');

  if (!email) {
    console.error('Usage: node src/scripts/diagnoseEmail.js <email> [--delete]');
    process.exit(1);
  }

  const MONGODB_URI = process.env.MONGODB_URI;
  if (!MONGODB_URI) {
    console.error('MONGODB_URI not set in env.');
    process.exit(1);
  }

  console.log(`\n🔍 Diagnostic email: ${email}`);
  console.log(`📡 Connecting to Mongo…`);
  await mongoose.connect(MONGODB_URI);
  console.log('✅ Connected.\n');

  const collections = [
    { name: 'Owner', model: Owner },
    { name: 'Sitter', model: Sitter },
    { name: 'Walker', model: Walker },
  ];

  let foundCount = 0;
  const ghostDocs = []; // verified=false → candidates for cleanup

  for (const { name, model } of collections) {
    // Recherche case-insensitive au cas où la normalisation aurait foiré
    // pour un ancien compte.
    const docs = await model
      .find({ email: new RegExp(`^${escapeRegex(email)}$`, 'i') })
      .select('_id email verified status name createdAt updatedAt')
      .lean();

    if (docs.length === 0) {
      console.log(`  · ${name.padEnd(8)} → none`);
      continue;
    }
    for (const d of docs) {
      foundCount += 1;
      console.log(`  · ${name.padEnd(8)} → ${d._id}`);
      console.log(`        email     : ${d.email}`);
      console.log(`        name      : ${d.name || '(empty)'}`);
      console.log(`        verified  : ${d.verified}`);
      console.log(`        status    : ${d.status || '(none)'}`);
      console.log(`        created   : ${d.createdAt}`);
      console.log(`        updated   : ${d.updatedAt}`);
      if (d.verified === false || d.verified === undefined) {
        ghostDocs.push({ model, id: d._id, collection: name });
      }
    }
  }

  console.log(`\n📊 Total comptes trouvés: ${foundCount}`);
  console.log(`👻 Comptes fantômes (verified=false): ${ghostDocs.length}`);

  if (ghostDocs.length > 0) {
    if (shouldDelete) {
      console.log(`\n🗑  --delete activé. Suppression des comptes fantômes…`);
      for (const g of ghostDocs) {
        await g.model.deleteOne({ _id: g.id });
        console.log(`  · Supprimé ${g.collection} ${g.id}`);
      }
      console.log(`\n✅ ${ghostDocs.length} compte(s) supprimé(s). L'email est maintenant libre.`);
    } else {
      console.log(`\n💡 Pour supprimer ces comptes fantômes et libérer l'email, relance :`);
      console.log(`   node src/scripts/diagnoseEmail.js ${email} --delete\n`);
    }
  } else if (foundCount > 0) {
    console.log(`\nℹ️  Tous les comptes trouvés sont vérifiés — l'email est légitimement utilisé.`);
  } else {
    console.log(`\n✅ Aucun compte trouvé pour cet email.`);
    console.log(`   Si le signup retourne quand même "email already used", c'est un bug ailleurs.`);
    console.log(`   Vérifie aussi le champ "username" ou autres uniques côté User schema.`);
  }

  await mongoose.disconnect();
  process.exit(0);
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

main().catch((e) => {
  console.error('❌ Erreur:', e);
  process.exit(1);
});
