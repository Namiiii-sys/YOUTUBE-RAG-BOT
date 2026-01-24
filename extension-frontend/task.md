Task: Switch from OpenAI to Free Tier LLM (Gemini)
Analyze 
ragmodel.py
 to understand current implementation
 Create Implementation Plan
 Update requirements.txt to replace OpenAI with Google GenAI dependencies
 Refactor 
ragmodel.py
 to use Google Gemini
 Verify changes
 Analyze 
ragmodel.py
 to understand current implementation
 Create Implementation Plan
 Update 
requirements.txt
 to replace OpenAI with Google GenAI dependencies
 Refactor 
ragmodel.py
 to use Google Gemini
 Verify changes
 Fix Extension UI Layout (Compressed View)
 Remove Login Screen to Isolate UI
 Remove Login Screen to Isolate UI
 Refine Prompt to Handle Greetings Gracefully
 formatting for bullets/text (Markdown)
 Auto-scroll and Immediate Input Clearing
 Handle Rate Limits (Add Retries)
 Switch to Generous Free Model (gemini-flash-lite-latest)
 Handle Greetings without Transcript
 Research Feasible Login System
Phase 2: Authentication (Firebase)
 Create Firebase Project & Get Config (User Action Required)
 Frontend: Install Firebase SDK & Configure 
firebase.ts
 Frontend: Create 
Login
 Component (Conditional Rendering)
 Backend: Install firebase-admin & Setup Middleware
Verify End-to-End Login Flow
Phase 3: Auth Refactor (Manifest V3 Compliance)
 User: Provide OAuth Client ID
 Manifest: Add identity permission
 Frontend: Refactor 
Login.tsx
 to use chrome.identity
 Frontend: Verify launchWebAuthFlow