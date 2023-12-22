# API Social Media

The RESTful API for social media platform that handles user and post managing.

## User Registration and Authentication:

- Users can register with their email and password to create an account.
- Users can login with their credentials and receive a token for authentication.
- Users can logout and invalidate their token.

## User Profile:
- Users can create and update their profile, including profile picture, bio, and other details.
- Users can retrieve their own profile and view profiles of other users.
- Users can search for users by username or city where they live.

## Follow/Unfollow:
- Users can follow and unfollow other users.
- Users can view the list of users they are following and the list of users following them.

## Post Creation and Retrieval:
- Users can create new posts with text content and media attachments (e.g., images).
- Users can retrieve posts by hashtags.

## Likes and Comments:
- Users can like and unlike posts. 
- Users can add comments to posts and view comments on posts.

## Installation with Docker
### Docker should be installed
```bash
git clone https://github.com/lobodInI/API-Social-Media
cd api-social-media
docker-compose build
docker-compose up
```

## How to install using GitHub

- Clone repository: git clone https://github.com/lobodInI/API-Social-Media
- Select folder: cd api-social-media
- Create venv: python -m venv venv
- Activate venv: source venv/bin/activate
- Install requirements: pip install -r requirements.txt
- Run: python manage.py runserver
- Create user via: user/register
- Get access token via: user/token

## Documentation
### When show documentation go to
```commandline
http://127.0.0.1:8000/api/doc/swagger/
```
