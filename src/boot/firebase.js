import firebase from "firebase/app";

import "firebase/auth";
import "firebase/database";


var firebaseConfig = {
  apiKey: "AIzaSyBss45sbN7lGUtLvZ-SnIIjzhTcq7owf6k",
  authDomain: "strategify-fdc5f.firebaseapp.com",
  databaseURL: "https://strategify-fdc5f-default-rtdb.firebaseio.com",
  projectId: "strategify-fdc5f",
  storageBucket: "strategify-fdc5f.appspot.com",
  messagingSenderId: "1019947070543",
  appId: "1:1019947070543:web:af80b9591dfe51c163663a"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);
let firebaseAuth = firebaseApp.auth()
let firebaseDb = firebaseApp.database()

export { firebaseAuth, firebaseDb }
