# HVZ

A system to manage household items.

## REST-API

### Return Structure

Always returns a JSON-Object, except when get all was called.

#### Structure:

|    Field   |                          Description                          |
|:----------:|---------------------------------------------------------------|
|    data    | The returned data                                             |
| hvz_status | String representation of the request status (see table below) |

#### Returned statuses:

| HTTP Status | Status String     |                                     Description                                     |
|:-----------:|-------------------|-------------------------------------------------------------------------------------|
|     200     | OK                | Request was successful                                                              |
|     201     | Created           | Request was successful, a resource was created                                      |
|     400     | Missing Parameter | Could not create resource, required paramter not provided                           |
|     400     | Already Exists    | Could not create or edit resource, a unique column already exists                   |
|     400     | In Use            | Could not delete resource, because resource is still referenced by another resource |
|     404     | Not Found         | Resource could not be found                                                         |

## Release 0.2.0

### Backend

- Column required amount
- Calculate needed amount

### Frontend

- Edit name on click
- save change on leave and close window (name, amount, needed amount)
- icon for delete product
- shopping list view
- improve mobile view
