document.addEventListener('DOMContentLoaded', () => {
    console.log('Place details page loaded');
    
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        displayError('No place ID specified in the URL');
        return;
    }
    
    // Check authentication and fetch place details
    checkAuthentication(placeId);
    
    // Function to extract the place ID from URL query parameters
    function getPlaceIdFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id');
    }
    
    // Function to get a cookie by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
    
    // Check user authentication
    function checkAuthentication(placeId) {
        const token = getCookie('token');
        const addReviewButton = document.getElementById('add-review-button');
        
        if (!token) {
            // User is not authenticated, hide add review button
            if (addReviewButton) {
                addReviewButton.style.display = 'none';
            }
        } else {
            // User is authenticated, show add review button
            if (addReviewButton) {
                addReviewButton.style.display = 'block';
            }
        }
        
        // Fetch place details regardless of authentication status
        fetchPlaceDetails(token, placeId);
    }
    
    // Fetch place details from API
    async function fetchPlaceDetails(token, placeId) {
        try {
            const headers = {
                'Content-Type': 'application/json'
            };
            
            // Add token to headers if available
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
            
            const response = await fetch(`/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: headers
            });
            
            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
                displayReviews(place.reviews);
                updateReviewLink(placeId);
            } else {
                console.error('Failed to fetch place details:', response.statusText);
                displayError('Failed to load place details. Please try again later.');
            }
        } catch (error) {
            console.error('Error fetching place details:', error);
            displayError('An error occurred while loading place details.');
        }
    }
    
    // Display place details in the UI
    function displayPlaceDetails(place) {
        const placeDetailsSection = document.getElementById('place-details');
        
        // Clear the example content
        placeDetailsSection.innerHTML = '';
        
        // Create place title
        const placeTitle = document.createElement('h2');
        placeTitle.textContent = place.title;
        placeDetailsSection.appendChild(placeTitle);
        
        // Create place info div
        const placeInfoDiv = document.createElement('div');
        placeInfoDiv.className = 'place-info';
        
        // Add host info if available
        if (place.owner) {
            const hostPara = document.createElement('p');
            hostPara.innerHTML = `<strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}`;
            placeInfoDiv.appendChild(hostPara);
        }
        
        // Add price
        const pricePara = document.createElement('p');
        pricePara.innerHTML = `<strong>Price:</strong> $${place.price} per night`;
        placeInfoDiv.appendChild(pricePara);
        
        // Add description if available
        if (place.description) {
            const descPara = document.createElement('p');
            descPara.innerHTML = `<strong>Description:</strong> ${place.description}`;
            placeInfoDiv.appendChild(descPara);
        }
        
        // Add amenities if available
        if (place.amenities && place.amenities.length > 0) {
            const amenitiesDiv = document.createElement('div');
            amenitiesDiv.className = 'amenities';
            
            const amenitiesTitle = document.createElement('h3');
            amenitiesTitle.textContent = 'Amenities';
            amenitiesDiv.appendChild(amenitiesTitle);
            
            const amenitiesList = document.createElement('ul');
            place.amenities.forEach(amenity => {
                const listItem = document.createElement('li');
                listItem.textContent = amenity.name;
                amenitiesList.appendChild(listItem);
            });
            
            amenitiesDiv.appendChild(amenitiesList);
            placeInfoDiv.appendChild(amenitiesDiv);
        }
        
        placeDetailsSection.appendChild(placeInfoDiv);
    }
    
    // Display reviews
    function displayReviews(reviews) {
        const reviewsSection = document.getElementById('reviews');
        
        // Clear existing reviews, but keep the heading
        const reviewsHeading = reviewsSection.querySelector('h3');
        reviewsSection.innerHTML = '';
        reviewsSection.appendChild(reviewsHeading);
        
        // If no reviews, display a message
        if (!reviews || reviews.length === 0) {
            const noReviewsMsg = document.createElement('p');
            noReviewsMsg.textContent = 'No reviews yet.';
            reviewsSection.appendChild(noReviewsMsg);
            return;
        }
        
        // Create a card for each review
        reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            
            const reviewText = document.createElement('p');
            reviewText.textContent = review.text;
            
            const reviewUser = document.createElement('p');
            // Handle case where user information might not be directly available
            let userName = 'Anonymous';
            if (review.user) {
                userName = `${review.user.first_name} ${review.user.last_name}`;
            } else if (review.user_id) {
                userName = `User ${review.user_id}`;
            }
            reviewUser.textContent = `- ${userName}`;
            
            const reviewRating = document.createElement('p');
            reviewRating.textContent = `Rating: ${review.rating}/5`;
            
            reviewCard.appendChild(reviewText);
            reviewCard.appendChild(reviewUser);
            reviewCard.appendChild(reviewRating);
            
            reviewsSection.appendChild(reviewCard);
        });
    }
    
    // Update the "Add Review" link to include the place ID
    function updateReviewLink(placeId) {
        const addReviewButton = document.querySelector('#add-review-button a');
        if (addReviewButton) {
            addReviewButton.href = `add_review.html?id=${placeId}`;
        }
    }
    
    // Display error message
    function displayError(message) {
        const placeDetailsSection = document.getElementById('place-details');
        
        // Clear content
        placeDetailsSection.innerHTML = '';
        
        // Create and display error message
        const errorTitle = document.createElement('h2');
        errorTitle.textContent = 'Error';
        
        const errorMsg = document.createElement('p');
        errorMsg.textContent = message;
        errorMsg.style.color = 'red';
        
        placeDetailsSection.appendChild(errorTitle);
        placeDetailsSection.appendChild(errorMsg);
    }
});