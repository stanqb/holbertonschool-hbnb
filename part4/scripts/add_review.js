document.addEventListener('DOMContentLoaded', () => {
    console.log('Add review page loaded');
    
    // Check authentication first
    const token = checkAuthentication();
    
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        displayError('No place ID specified in the URL');
        return;
    }
    
    // Fetch place details to show place name
    fetchPlaceDetails(token, placeId);
    
    // Setup review form event listener
    setupReviewForm(token, placeId);
    
    // Function to check user authentication
    function checkAuthentication() {
        const token = getCookie('token');
        
        // If no token is found, redirect to index page
        if (!token) {
            window.location.href = 'index.html';
            return null;
        }
        
        return token;
    }
    
    // Function to get a cookie by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }
    
    // Function to extract the place ID from URL query parameters
    function getPlaceIdFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('id');
    }
    
    // Function to fetch place details to show place name
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
                
                // Update place name in the heading
                const placeNameElement = document.getElementById('place-name');
                if (placeNameElement && place.title) {
                    placeNameElement.textContent = place.title;
                }
            } else {
                console.error('Failed to fetch place details:', response.statusText);
                displayError('Failed to load place details. Please try again later.');
            }
        } catch (error) {
            console.error('Error fetching place details:', error);
            displayError('An error occurred while loading place details.');
        }
    }
    
    // Function to setup the review form event listener
    function setupReviewForm(token, placeId) {
        const reviewForm = document.getElementById('review-form');
        
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                
                // Get form data
                const reviewText = document.getElementById('review').value;
                const rating = document.getElementById('rating').value;
                
                // Validate the form data
                if (!reviewText.trim()) {
                    alert('Please enter a review text.');
                    return;
                }
                
                if (!rating) {
                    alert('Please select a rating.');
                    return;
                }
                
                // Submit the review
                await submitReview(token, placeId, reviewText, rating);
            });
        }
    }
    
    // Function to submit the review to the API
    async function submitReview(token, placeId, reviewText, rating) {
        try {
            const response = await fetch('/api/v1/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    text: reviewText,
                    rating: parseInt(rating, 10),
                    place_id: placeId
                })
            });
            
            if (response.ok) {
                // Display success message
                alert('Review submitted successfully!');
                
                // Clear the form
                document.getElementById('review').value = '';
                document.getElementById('rating').value = '';
                
                // Redirect back to the place details page
                window.location.href = `place.html?id=${placeId}`;
            } else {
                // Handle error response
                const errorData = await response.json();
                
                if (errorData.error) {
                    alert(`Failed to submit review: ${errorData.error}`);
                } else {
                    alert('Failed to submit review. Please try again later.');
                }
            }
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('An error occurred while submitting the review. Please try again later.');
        }
    }
    
    // Function to display an error message
    function displayError(message) {
        const addReviewSection = document.querySelector('.add-review');
        
        // Clear content
        if (addReviewSection) {
            addReviewSection.innerHTML = '';
            
            // Create and display error message
            const errorTitle = document.createElement('h2');
            errorTitle.textContent = 'Error';
            
            const errorMsg = document.createElement('p');
            errorMsg.textContent = message;
            errorMsg.style.color = 'red';
            
            addReviewSection.appendChild(errorTitle);
            addReviewSection.appendChild(errorMsg);
        }
    }
});