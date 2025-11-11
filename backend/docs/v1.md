# API Documentation

## Overview

This document provides a comprehensive guide to the FastAPI-based API for managing users, cars, and orders in a car sales system. The API follows RESTful principles and uses OpenAPI 3.1.0 specifications.

- **Title**: FastAPI
- **Version**: 0.1.0
- **Base URL**: `/api/backend`
- **Authentication**: OAuth2 Password Bearer (see [Authentication](#authentication) section)
- **Content Type**: `application/json` for most requests/responses
- **Error Handling**: Validation errors return HTTP 422 with a body containing `detail` (array of `{loc: array, msg: string, type: string}`)

Endpoints are grouped by resource: **Users**, **Cars**, and **Orders**. Cars appear to be publicly accessible (no auth required), while Orders require authentication.

## Authentication

The API uses OAuth2 with password grant type for token-based authentication. Protected endpoints (e.g., `/users/me`, all Orders) require an `Authorization: Bearer <access_token>` header.

### Login for Access Token

- **Endpoint**: `POST /users/token`
- **Request Body** (form-urlencoded):
  - `username` (required, string): User's username
  - `password` (required, string): User's password
  - `grant_type` (optional, string, default: "password"): Must be "password"
  - `scope` (optional, string, default: ""): Empty string
  - `client_id` (optional, string or null)
  - `client_secret` (optional, string or null)
- **Responses**:
  - **200 OK**:

    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```

  - **422 Unprocessable Entity**: Validation error (e.g., invalid credentials)

### Read Current User

- **Endpoint**: `GET /users/me`
- **Requires Auth**: Yes
- **Responses**:
  - **200 OK**:

    ```json
    {
      "username": "string",
      "email": "string",
      "id": 0,
      "is_active": true,
      "created_at": "2025-11-11T10:23:00",
      "updated_at": "2025-11-11T10:23:00"  // optional
    }
    ```

## Users

### Signup

- **Endpoint**: `POST /users/signup`
- **Requires Auth**: No
- **Request Body**:

  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```

- **Responses**:
  - **201 Created**:

    ```json
    {
      "username": "string",
      "email": "string",
      "id": 0,
      "is_active": true,
      "created_at": "2025-11-11T10:23:00",
      "updated_at": "2025-11-11T10:23:00"  // optional
    }
    ```

  - **422 Unprocessable Entity**: Validation error (e.g., duplicate username/email)

## Cars

Cars represent vehicle listings with detailed specs. All operations are public (no auth required).

### Create New Car

- **Endpoint**: `POST /cars/`
- **Request Body**:

  ```json
  {
    "brand": "string",
    "model": "string",
    "year": 0,
    "body_type": "string",
    "engine_type": "string",
    "engine_size_liters": 0.0,
    "horsepower": 0,
    "transmission": "string",
    "fuel_type": "string",
    "mileage_km": 0,
    "top_speed_kmh": 0,
    "color": "string",
    "features": "string",
    "price_usd": 0.0,
    "discount_percent": 0.0,
    "num_in_stock": 0,
    "description": "string"
  }
  ```

- **Responses**:
  - **201 Created**:

    ```json
    {
      "brand": "string",
      "model": "string",
      "year": 0,
      "body_type": "string",
      "engine_type": "string",
      "engine_size_liters": 0.0,
      "horsepower": 0,
      "transmission": "string",
      "fuel_type": "string",
      "mileage_km": 0,
      "top_speed_kmh": 0,
      "color": "string",
      "features": "string",
      "price_usd": 0.0,
      "discount_percent": 0.0,
      "num_in_stock": 0,
      "description": "string",
      "id": 0
    }
    ```

  - **422 Unprocessable Entity**: Validation error

### Read Cars (List)

- **Endpoint**: `GET /cars/`
- **Query Parameters**:
  - `skip` (optional, integer, default: 0): Number of records to skip
  - `limit` (optional, integer, default: 100): Maximum number of records to return
- **Responses**:
  - **200 OK**: Array of Car objects (see Create New Car for schema)

### Read Car (By ID)

- **Endpoint**: `GET /cars/{car_id}`
- **Path Parameters**:
  - `car_id` (required, integer): The car ID
- **Responses**:
  - **200 OK**: Single Car object
  - **422 Unprocessable Entity**: Validation error (e.g., invalid ID)

### Update Existing Car

- **Endpoint**: `PUT /cars/{car_id}`
- **Path Parameters**:
  - `car_id` (required, integer): The car ID
- **Request Body**: Partial Car (all fields optional):

  ```json
  {
    "brand": "string",  // optional
    // ... other fields optional or null
  }
  ```

- **Responses**:
  - **200 OK**: Updated Car object
  - **422 Unprocessable Entity**: Validation error

### Delete Existing Car

- **Endpoint**: `DELETE /cars/{car_id}`
- **Path Parameters**:
  - `car_id` (required, integer): The car ID
- **Responses**:
  - **204 No Content**: Success (no body)
  - **422 Unprocessable Entity**: Validation error

## Orders

Orders represent user purchases of cars. All operations require authentication.

### Create New Order

- **Endpoint**: `POST /orders/`
- **Requires Auth**: Yes
- **Request Body**:

  ```json
  {
    "car_ids": [0]  // array of integers (car IDs)
  }
  ```

- **Responses**:
  - **201 Created**:

    ```json
    {
      "id": 0,
      "created_at": "2025-11-11T10:23:00",
      "user_id": 0,
      "cars": [  // array of full Car objects
        {
          // Full Car schema (see Cars section)
        }
      ]
    }
    ```

  - **422 Unprocessable Entity**: Validation error (e.g., invalid car IDs)

### Read Orders (List)

- **Endpoint**: `GET /orders/`
- **Requires Auth**: Yes
- **Query Parameters**:
  - `skip` (optional, integer, default: 0): Number of records to skip
  - `limit` (optional, integer, default: 100): Maximum number of records to return
- **Responses**:
  - **200 OK**: Array of Order objects (see Create New Order for schema)
  - **422 Unprocessable Entity**: Validation error

### Read Order (By ID)

- **Endpoint**: `GET /orders/{order_id}`
- **Requires Auth**: Yes
- **Path Parameters**:
  - `order_id` (required, integer): The order ID
- **Responses**:
  - **200 OK**: Single Order object
  - **422 Unprocessable Entity**: Validation error

### Update Existing Order

- **Endpoint**: `PUT /orders/{order_id}`
- **Requires Auth**: Yes
- **Path Parameters**:
  - `order_id` (required, integer): The order ID
- **Request Body**: Partial Order (fields optional):

  ```json
  {
    "car_ids": [0]  // optional array of integers
  }
  ```

- **Responses**:
  - **200 OK**: Updated Order object
  - **422 Unprocessable Entity**: Validation error

### Delete Existing Order

- **Endpoint**: `DELETE /orders/{order_id}`
- **Requires Auth**: Yes
- **Path Parameters**:
  - `order_id` (required, integer): The order ID
- **Responses**:
  - **204 No Content**: Success (no body)
  - **422 Unprocessable Entity**: Validation error

## Root Endpoint

- **Endpoint**: `GET /`
- **Requires Auth**: No
- **Summary**: Health check or root info
- **Responses**:
  - **200 OK**: Empty JSON object `{}`
