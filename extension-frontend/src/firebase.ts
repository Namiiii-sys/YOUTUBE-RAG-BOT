import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyCAl93O-tITw6p_sWNxm2OM0aXf0oPQNo4",
    authDomain: "assistant-bot-0.firebaseapp.com",
    projectId: "assistant-bot-0",
    storageBucket: "assistant-bot-0.firebasestorage.app",
    messagingSenderId: "1024726801843",
    appId: "1:1024726801843:web:0388c6ffaa5d00db383fc6",
    measurementId: "G-NQC8CXVBV8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Export Auth Service
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
