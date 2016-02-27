## Packages Used in this project
### Database
1. postgres alon with postgis

### Backend API 
1. django rest framework
2. django rest framework gis

### API documentation
1. django rest swagger 

### Notes
* there is no caching is being used as of now. but we can use memcached or redis for storing search results
* to search a point in given service area, i have used bbcontains (bounding box contains) geodjango filter