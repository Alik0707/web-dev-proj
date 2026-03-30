The project is a merit-based system for distributing government subsidies to agricultural producers. Instead of a first-come, first-served approach, a machine leardning model is used to evaluate each application based on farm data, its performance, and history.

The user (agricultural producer or operator) submits an application through a web interface, specifying key characteristics such as region, production volume, financial indicators, and other relevant information. This data is sent to the backend, where a ready-made ML model is integrated. The model calculates the final score and generates an explanation of the factors that influenced the outcome.

The system stores applications, scoring results, and history, and then ranks all applicants. Based on this data, a shortlist of candidates recommended for subsidies is created. The final decision rests with the commission, but the system significantly simplifies and objectively simplifies the selection process.

The frontend is implemented in Angular and provides:

user authentication (JWT) for the application form, viewing the list of applicants, displaying the score and its explanation, and viewing the shortlist of candidates.

The backend is built on the Django REST Framework:

processes API requests, manages data (applications, indicators, subsidy history), integrates an ML model for scoring calculations, and implements authorization and CRUD operations.

As a result, the system makes the subsidy distribution process more transparent, fair, and data-driven, reducing the influence of queue management and human error.
