const express = require('express');

const { createTask, getTasks, deleteTask } = require('../controllers/taskController');
const { requireAuth, requireRole } = require('../middleware/auth');

const router = express.Router();

/**
 * @swagger
 * /tasks:
 *   get:
 *     summary: Get all tasks (Owner only)
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Tasks retrieved successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 tasks:
 *                   type: array
 *                   items:
 *                     type: object
 *       401:
 *         description: Unauthorized
 *       403:
 *         description: Only owners can access this endpoint
 */
router.get('/', requireAuth, requireRole('owner'), getTasks);

/**
 * @swagger
 * /tasks:
 *   post:
 *     summary: Create a new task (Owner only)
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - title
 *             properties:
 *               title:
 *                 type: string
 *                 example: Feed the dog
 *               description:
 *                 type: string
 *                 example: Feed Max at 6 PM
 *               completed:
 *                 type: boolean
 *                 example: false
 *     responses:
 *       201:
 *         description: Task created successfully
 *       400:
 *         description: Invalid input
 *       401:
 *         description: Unauthorized
 *       403:
 *         description: Only owners can create tasks
 */
router.post('/', requireAuth, requireRole('owner'), createTask);

/**
 * @swagger
 * /tasks/{id}:
 *   delete:
 *     summary: Delete a task by id (Owner only — own tasks)
 *     tags: [Tasks]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema: { type: string }
 *     responses:
 *       200: { description: Task deleted }
 *       404: { description: Task not found or not owned by user }
 *
 * v23.1.147 — Daniel : "Cómo se pueden eliminar las tareas?".
 */
router.delete('/:id', requireAuth, requireRole('owner'), deleteTask);

module.exports = router;

