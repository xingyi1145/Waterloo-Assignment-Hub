# **Project Charter — Waterloo CS Study Note Hub**

## **1. Project Title**

**Waterloo CS Study Note Hub (WCSNH)**

---

## **2. Project Overview**

The Waterloo CS Study Note Hub is a peer-to-peer knowledge sharing platform designed to help students organize, share, and find high-quality study materials for University of Waterloo CS courses. Instead of traditional assignment grading, this platform focuses on collaborative learning through shared Markdown-based notes, cheat sheets, and course summaries. Professors can structure courses into topics, while students submit content to help their peers succeed.

---

## **3. Project Goals & Objectives**

### **Primary Goals**

* Provide a centralized repository for student-generated study materials.
* Allow students to write and view rich text notes using Markdown.
* Organize content hierarchically: Courses -> Topics -> Study Notes.
* Encourage quality content through a community feedback system (likes & comments).

### **Secondary Goals**

* Foster a collaborative study environment.
* Create a modern, scalable full-stack project suitable for portfolio use.
* Support various resource types (Cheat Sheets, Summaries, Guides).

---

## **4. Scope**

### **In Scope**

* User authentication system (username + password).
* User roles: **Student** and **Professor**.
* Course and Topic management.
* Web-based Markdown editor and renderer for notes.
* Resource categorization (CheatSheet, Summary, Guide).
* Recursive comment system or linear discussion threads.
* "Like" system for curating top resources.

### **Out of Scope**

* Code execution or auto-grading (removed from previous scope).
* Plagiarism detection.
* Integration with official University systems.

---

## **5. Stakeholders**

| Role                | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| **Student Users**   | Create notes, browse topics, rate content.                  |
| **Professor Users** | Create courses and topics. moderate content.                |
| **Developer (You)** | Builds and maintains the platform.                          |

---

## **6. System Overview / Experience**

### **Core Workflows**

1.  **Professor** creates a Course (e.g., "CS 137") and adds Topics (e.g., "Pointers", "Recursion").
2.  **Student** enrolls in the course.
3.  **Student** navigates to "Recursion" and clicks "Create Note".
4.  **Student** writes a "Recursion Cheat Sheet" in Markdown and tags it as a CheatSheet.
5.  **Other Students** view the note, find it helpful, and leave a "Like" or a clarifying comment.

