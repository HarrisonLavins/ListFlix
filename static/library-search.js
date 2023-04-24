/* 
Created on Sat Apr 22 12:05:53 2023
@author: harrisonlavins
-----------------------
Define the behavior of the library search components
*/

//Handles search form logic
const searchMovies = function (event) {
  const result = alert('Searching TMDB Movies... popping popcorn...');
  event.preventDefault();
};

// your form
const form = document.getElementById('search-form');

// attach event listener
form.addEventListener('submit', searchMovies, true);
