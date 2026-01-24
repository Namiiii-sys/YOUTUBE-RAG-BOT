import { GoogleAuthProvider, signInWithCredential } from "firebase/auth";
import { auth } from "../firebase";
import { FcGoogle } from "react-icons/fc";

const Login = () => {
  const handleLogin = async () => {
    try {
      // 1. Launch Chrome's native auth flow
      // This respects the CSP because it opens a separate, secure browser window
      const redirectUri = chrome.identity.getRedirectURL();

      const clientId = "1024726801843-mbgbk5tnotjsf422mp5gfocnpi3ledvl.apps.googleusercontent.com";
      const authUrl = `https://accounts.google.com/o/oauth2/auth?client_id=${clientId}&response_type=id_token&redirect_uri=${encodeURIComponent(redirectUri)}&scope=openid%20email%20profile&nonce=${Date.now()}`;

      chrome.identity.launchWebAuthFlow(
        {
          url: authUrl,
          interactive: true,
        },
        async (responseUrl) => {
          if (chrome.runtime.lastError || !responseUrl) {
            console.error("Auth flow failed:", chrome.runtime.lastError);
            return;
          }

          // 2. Extract ID token from the redirect URL
          const url = new URL(responseUrl);
          const params = new URLSearchParams(url.hash.substring(1)); // Google returns token in hash fragment
          const idToken = params.get("id_token");

          if (!idToken) {
            console.error("No ID token found in response");
            return;
          }

          // 3. Sign in to Firebase with the ID token
          const credential = GoogleAuthProvider.credential(idToken);
          await signInWithCredential(auth, credential);
          console.log("Successfully logged in with Chrome Identity!");
        }
      );

    } catch (error) {
      console.error("Login failed", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full w-full bg-white p-6 text-center">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Welcome Back!</h1>
      <p className="text-gray-500 mb-8">Sign in to continue chatting with your video assistant.</p>

      <button
        onClick={handleLogin}
        className="flex items-center gap-3 px-6 py-3 bg-white border border-gray-300 rounded-xl shadow-sm hover:bg-gray-50 transition-all text-gray-700 font-medium w-full justify-center"
      >
        <FcGoogle className="text-2xl" />
        <span>Sign in with Google</span>
      </button>
    </div>
  );
};

export default Login;
