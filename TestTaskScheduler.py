import unittest
from tkinter import Tk
from tkinter.messagebox import _show
from unittest.mock import patch
from tkinter import messagebox
from unittest.mock import MagicMock


from TaskScheduler import Task, Scheduler, TaskSchedulerGUI, LinkedList

class TestTaskScheduler(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = TaskSchedulerGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch.object(messagebox, 'showinfo')
    def test_add_task(self, mocked_info):
        initial_tasks_count = len(self.app.scheduler.tasks.display_tasks())
        self.app.title_entry.insert(0, "Test Task")
        self.app.desc_entry.insert(0, "Test Description")
        self.app.due_entry.insert(0, "2024-04-08")
        self.app.priority_entry.insert(0, "1")

        self.app.add_task()
        mocked_info.assert_called_once()

        final_tasks_count = len(self.app.scheduler.tasks.display_tasks())

        self.assertEqual(final_tasks_count, initial_tasks_count + 1)

    def test_remove_task(self):
        # Add some tasks to the scheduler
        task1 = Task("Task 1", "Description 1", "2024-04-08", 1)
        task2 = Task("Task 2", "Description 2", "2024-04-09", 2)
        task3 = Task("Task 3", "Description 3", "2024-04-10", 3)
        self.app.scheduler.add_task(task1)
        self.app.scheduler.add_task(task2)
        self.app.scheduler.add_task(task3)

        # Remove a task
        self.app.scheduler.remove_task(task2)

        # Get the tasks after removal
        tasks_after_removal = self.app.scheduler.tasks.display_tasks()

        # Check if the removed task is not present in the tasks list
        self.assertNotIn(task2, tasks_after_removal)

    def test_undo_redo(self):
        task1 = Task("Task 1", "Description 1", "2024-04-08", 1)
        task2 = Task("Task 2", "Description 2", "2024-04-09", 2)
        self.app.scheduler.add_task(task1)
        self.app.scheduler.add_task(task2)

        self.assertEqual(len(self.app.scheduler.tasks.display_tasks()), 2)

        self.app.scheduler.undo()
        self.assertEqual(len(self.app.scheduler.tasks.display_tasks()), 1)

        self.app.scheduler.redo()
        self.assertEqual(len(self.app.scheduler.tasks.display_tasks()), 2)

    def test_refresh_tasks(self):
        # Create some sample tasks
        task1 = Task("Task 1", "Description 1", "2024-04-08", 1)
        task2 = Task("Task 2", "Description 2", "2024-04-09", 2)
        task3 = Task("Task 3", "Description 3", "2024-04-10", 3)

        # Mock the tasks in the Scheduler
        self.app.scheduler.tasks.display_tasks = MagicMock(return_value=[task1, task2, task3])

        # Call refresh_tasks()
        self.app.refresh_tasks()

        # Check if the tasks_listbox is updated correctly
        expected_display = ["Task 1 - 2024-04-08", "Task 2 - 2024-04-09", "Task 3 - 2024-04-10"]
        actual_display = [self.app.tasks_listbox.get(i) for i in range(self.app.tasks_listbox.size())]

        self.assertEqual(actual_display, expected_display)

        def test_selection_sort(self):
            # Create unsorted tasks
            task1 = Task("Task 1", "Description 1", "2024-04-08", 3)
            task2 = Task("Task 2", "Description 2", "2024-04-09", 1)
            task3 = Task("Task 3", "Description 3", "2024-04-10", 2)

            # Create a linked list and append unsorted tasks
            linked_list = LinkedList()
            linked_list.append(task1)
            linked_list.append(task2)
            linked_list.append(task3)

            # Sort the linked list
            linked_list.selection_sort()

            # Retrieve the sorted tasks
            sorted_tasks = linked_list.display_tasks()

            # Check if tasks are sorted correctly based on priority
            self.assertEqual(sorted_tasks[0].priority, 1)  # Task 2 has the lowest priority
            self.assertEqual(sorted_tasks[1].priority, 2)  # Task 3 has the next lowest priority
            self.assertEqual(sorted_tasks[2].priority, 3)  # Task 1 has the highest priority

    def test_selection_sort(self):
        # Create unsorted tasks
        task1 = Task("Task 1", "Description 1", "2024-04-08", 3)
        task2 = Task("Task 2", "Description 2", "2024-04-09", 1)
        task3 = Task("Task 3", "Description 3", "2024-04-10", 2)

        # Create a linked list and append unsorted tasks
        linked_list = LinkedList()
        linked_list.append(task1)
        linked_list.append(task2)
        linked_list.append(task3)

        # Sort the linked list
        linked_list.selection_sort()

        # Retrieve the sorted tasks
        sorted_tasks = linked_list.display_tasks()

        # Check if tasks are sorted correctly based on priority
        self.assertEqual(sorted_tasks[0].priority, 1)  # Task 2 has the lowest priority
        self.assertEqual(sorted_tasks[1].priority, 2)  # Task 3 has the next lowest priority
        self.assertEqual(sorted_tasks[2].priority, 3)  # Task 1 has the highest priority
if __name__ == '__main__':
    unittest.main()