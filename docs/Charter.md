# **Project Charter — SE-StudyCenter**

## **1. Project Title**

**SE-StudyCenter**

---

## **2. Project Overview**

The SE-StudyCenter is a peer-to-peer knowledge sharing platform designed to help students organize, share, and find high-quality study materials for University of Waterloo CS courses. Instead of traditional assignment grading, this platform focuses on collaborative learning through shared Markdown-based notes, cheat sheets, and course summaries. Professors can structure courses into topics, while students submit content to help their peers succeed.

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
* Support various note types (Summary, Lecture, Code, Other).

---

## **4. Scope**

### **In Scope**

* User authentication system (username + password).
* User roles: **Student** and **Professor**.
* Course and Topic management.
* **Dual-pane Markdown editor** for creating rich notes.
* **Card-based UI** for browsing notes within topics.
* **Table of Contents** sidebar generated automatically from note headers.
* "Like" system and Comment threads.

### **Out of Scope**

* Code execution or auto-grading.
* Plagiarism detection.
* Integration with official University systems.

---

## **5. Stakeholders**

| Role                | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| **Student Users**   | Create notes (summaries/guides), view card feed, like/comment.|
| **Professor Users** | Create courses and topics. moderate content.                |
| **Developer (You)** | Builds and maintains the platform.                          |

---

## **6. System Overview / Experience**

### **Core Workflows**

1.  **Professor** creates a Course (e.g., "CS 137") and adds Topics (e.g., "Pointers", "Recursion").
2.  **Student** enrolls in the course and selects a Topic.
3.  **Student** clicks "Create Note", types in Markdown with live preview, and selects "Summary" type.
4.  **Student** submits note, which appears as a Card with a specialized badge.
5.  **Peers** click the card, navigate via the TOC sidebar, and leave likes or comments.

