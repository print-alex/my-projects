// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { GoogleAuthProvider, getAuth } from "firebase/auth";
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDJ5M-MYchM92s8aGqWpUMf8obAmUlzxg0",
  authDomain: "uberx-d338d.firebaseapp.com",
  projectId: "uberx-d338d",
  storageBucket: "uberx-d338d.appspot.com",
  messagingSenderId: "733719600958",
  appId: "1:733719600958:web:e2f334d46104693f65966f",
  measurementId: "G-EGY1FHHBWL"
}; 

// Initialize Firebase
const app = initializeApp(firebaseConfig)
const provider = new GoogleAuthProvider()
const auth = getAuth()

export{ app, provider,auth }