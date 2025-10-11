# SkillBridge – Personalized Learning Path Generator  
**Tagline:** “Bridging skills to careers with AI-guided learning.”

---

## 1. Project Title  
**SkillBridge – Personalized Learning Path Generator**

---

## 2. Team Members  
- Sera  
- Adrina  
- Rahul  
- Senorita  
- Alan  

---

## 3. Problem Statement  
Learners often struggle to identify the right sequence of courses, projects, and resources to acquire new skills or pursue a career. Scattered online materials, inconsistent guidance, and lack of personalized learning paths lead to wasted time, confusion, and demotivation.  
**SkillBridge** aims to provide AI-generated, step-by-step learning roadmaps tailored to each user’s knowledge level, goals, and learning pace, ensuring efficient skill acquisition and career readiness.

---

## 4. Core Components  

### **UI**
- Web App (React.js) and Mobile App (React Native)  
- Input forms for career/skill goal, current knowledge level, and learning preferences  
- Visual roadmap/dashboard displaying learning steps, milestones, and recommended resources  

### **LLM API**
- OpenAI GPT API (or similar) to generate structured learning paths  
- Converts user goals and inputs into a step-by-step learning roadmap  
- Integrates with a knowledge base of courses, tutorials, books, and projects  

### **Tools**
- **Database:** MongoDB to store user profiles, learning paths, and progress  
- **Visualization Library:** D3.js or Chart.js to display roadmap timelines and milestones  
- **Notification System (optional):** Email or push notifications for milestones or reminders  
- **Backend:** Node.js / Express.js for handling requests and storing data  

---

## 5. LLM’s Primary Task  
- Understand user goals, current knowledge level, and preferences  
- Generate personalized step-by-step learning plans  
- Recommend resources, projects, and milestones  
- Adapt roadmap dynamically if user progress or inputs change  

---

## 6. Inputs and Outputs  

### **Input:**
- User skill or career goal (e.g., “Data Scientist”)  
- Current knowledge level (Beginner / Intermediate / Advanced)  
- Available learning time per week  
- Optional learning style preferences (video, reading, hands-on)  

### **Output:**
- Structured, personalized learning roadmap with:  
  - Sequential steps with estimated durations  
  - Recommended resources (courses, books, tutorials, projects)  
  - Milestones for progress tracking  
  - Optional visual roadmap (timeline or flowchart)  

---

## 7. Expected Outcome  
- Clear, actionable guidance for skill acquisition  
- Efficient, personalized learning paths reducing wasted time  
- Increased user motivation and confidence  
- Easy tracking of progress and milestones  
- Scalable system adaptable to any skill or career path  

---

## 8. System Diagram
### [User Device: Web/Mobile App] 
###         | 
###         v 
### [UI: Input Form + Roadmap Dashboard] 
###         | 
###         v 
### [LLM API + Knowledge Base] 
###         | 
###         v 
### [Backend Decision Engine] ---> [Database: User Profiles, Roadmaps] 
###         | 
###         v 
### [Visual Roadmap / Notifications to User]
