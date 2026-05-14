import { Router } from "express";
import {
  getTodos,
  getTodo,
  createTodo,
  updateTodo,
  deleteTodo,
  getPaginatedTodos,
  getStats,
} from "../controllers/todo.controller";
import {
  validateTodoCreate,
  validateTodoUpdate,
  validateId,
} from "../middlewares/validate.middleware";

const router = Router();

router.get("/", getTodos);

router.get("/paginated", getPaginatedTodos);

router.get("/stats", getStats);

router.get("/:id", validateId, getTodo);

router.post("/", validateTodoCreate, createTodo);

router.put("/:id", validateId, validateTodoUpdate, updateTodo);

router.patch("/:id", validateId, validateTodoUpdate, updateTodo);

router.delete("/:id", validateId, deleteTodo);

export default router;
