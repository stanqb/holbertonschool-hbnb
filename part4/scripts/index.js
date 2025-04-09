document.addEventListener('DOMContentLoaded', () => {
    console.log('Index page loaded');
    
    // Function to get a cookie by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
    
    // Check user authentication
    function checkAuthentication() {
        const token = getCookie('token');
        const loginLink = document.getElementById('login-link');
        
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
        
        // Fetch places data regardless of authentication status
        fetchPlaces(token);
    }
    
    // Fetch places data from API
    async function fetchPlaces(token) {
        try {
            const headers = {
                'Content-Type': 'application/json'
            };
            
            // Add token to headers if available
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                method: 'GET',
                headers: headers
            });
            
            if (response.ok) {
                const places = await response.json();
                displayPlaces(places);
                // Store places in a global variable for filtering
                window.allPlaces = places;
                setupPriceFilter();
            } else {
                console.error('Failed to fetch places:', response.statusText);
                displayError('Failed to load places. Please try again later.');
            }
        } catch (error) {
            console.error('Error fetching places:', error);
            displayError('An error occurred while loading places.');
        }
    }
    
    // Display places in the UI
    function displayPlaces(places) {
        const placesListSection = document.getElementById('places-list');
        
        // Clear the example place cards (keeping only the heading)
        const heading = placesListSection.querySelector('h2');
        placesListSection.innerHTML = '';
        placesListSection.appendChild(heading);
        
        // If no places, display a message
        if (!places || places.length === 0) {
            const noPlacesMsg = document.createElement('p');
            noPlacesMsg.textContent = 'No places available at the moment.';
            placesListSection.appendChild(noPlacesMsg);
            return;
        }
        
        // Create a card for each place
        places.forEach(place => {
            const placeCard = document.createElement('div');
            placeCard.className = 'place-card';
            placeCard.dataset.price = place.price; // Add price as a data attribute for filtering
            
            const placeTitle = document.createElement('h3');
            placeTitle.textContent = place.title;
            
            const placePrice = document.createElement('p');
            placePrice.textContent = `$${place.price} per night`;
            
            const detailsButton = document.createElement('a');
            detailsButton.href = `place.html?id=${place.id}`;
            detailsButton.className = 'details-button';
            detailsButton.textContent = 'View Details';
            
            placeCard.appendChild(placeTitle);
            placeCard.appendChild(placePrice);
            placeCard.appendChild(detailsButton);
            
            placesListSection.appendChild(placeCard);
        });
    }
    
    // Setup price filter functionality
    function setupPriceFilter() {
        const priceFilter = document.getElementById('price-filter');
        
        priceFilter.addEventListener('change', (event) => {
            const maxPrice = event.target.value;
            const placesListSection = document.getElementById('places-list');
            const placeCards = placesListSection.querySelectorAll('.place-card');
            
            placeCards.forEach(card => {
                const price = parseFloat(card.dataset.price);
                
                if (maxPrice === 'all' || price <= parseFloat(maxPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Display error message
    function displayError(message) {
        const placesListSection = document.getElementById('places-list');
        
        // Clear content except heading
        const heading = placesListSection.querySelector('h2');
        placesListSection.innerHTML = '';
        placesListSection.appendChild(heading);
        
        // Create and display error message
        const errorMsg = document.createElement('p');
        errorMsg.textContent = message;
        errorMsg.style.color = 'red';
        placesListSection.appendChild(errorMsg);
    }
    
    // Initialize page
    checkAuthentication();
});