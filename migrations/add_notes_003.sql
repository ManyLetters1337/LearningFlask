use base;


INSERT INTO notes (note_uuid, user_id, title, description, status, created_on)
    VALUES ("d61757ee-0765-11ea-a36e-74d435ecfdb9",
    1,
    "Flask",
    "Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.[3] It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself.",
    False,
    now()
    );


INSERT INTO notes (note_uuid, user_id, title, description, status, created_on)
    VALUES ("3a7f2320-0765-11ea-a36e-74d435ecfdb9",
    1,
    "Jinja",
    "Jinja is a web template engine for the Python programming language and is licensed under a BSD License created by Armin Ronacher. It is similar to the Django template engine but provides Python-like expressions while ensuring that the templates are evaluated in a sandbox. It is a text-based template language and thus can be used to generate any markup as well as sourcecode.",
    False,
    now()
    );