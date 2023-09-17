# Google Map Application with Vue.js

## Project Description
This project is a simple web application built in Vue.js that displays the Google Map and its 
user interfaces. It has the following features:

- A button to allow users to acquire their current location from their browser.
- A search module that lets users enter the name of a location. The search feature is triggered 
  by both button clicks and pressing the enter key on the keyboard.
- Display the location on a map and add a marker to each searched location every time the 
  location changes.
- A table with pagination to show all searched places:
  - Display a maximum of 10 records on each page.
  - A checkbox at the beginning of each row to let users select multiple records at the same time.
  - A delete button on the top to remove all selected records as well as their markers on the map.

## Instructions to Run the Program
Make sure `npm` is installed in your local machine. Clone the project to your local machine. Add
an `.env` file to your project folder and add the following credentials
```
VITE_API_KEY=$you_google_map_api_key
```

Run the following command inside the project folder
```bash
npm install
npm run dev
```

Open your browser and navigate to the URL http://localhost:3000/

Thank you for using this app :blush: