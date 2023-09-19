# CONTRIBUTING

Contributing to the HNGx Event App.

Thank you for considering contributing to the HNGx Event Application! We welcome contributions from the community to help improve and maintain this project. Before you start working on your contribution, please read and follow these guidelines.

# Getting Started

To contribute to this project, follow these steps:

1. Fork the repository to your own GitHub account.

2. Clone the forked repository to your local machine:
```
git clone https://github.com/hngx-org/Piranha-events-backend.git

```

3. Create a new branch for your changes:
```
git checkout -b <your_feature_name>
```

4. Make your desired changes to the codebase.

5. Commit your changes with descriptive commit messages:
```
git commit -m "Add new feature" -m "Description of the changes made."
```

6. Push your changes to your forked repository:
```
git push origin <your_feature_name>
```

7 .Create a pull request (PR) to the main repository with your changes.

## Code Style

Please adhere to the following coding guidelines:

- Follow the PEP 8 style guide for Python code. Please make sure your code is formatted according to the standards and conventions described in this guide. You can use tools like [pycodestyle](https://pypi.org/project/pycodestyle/) to check for styling error and  [autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8) to automatically format your code.
  
- We useCapWords convention(no underscore) E.g. `EventPlanner` instead of `Event_Planner` or `Event_planner`. For model's attributes, we use snake_case e.g. `first_name`, `last_name` instead of camelCase. Field names should be all lowercase. See [Django Documentations](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/) for guidance.

- Write clear and concise commit messages

Please follow this convention when you write or modify any code in this project.

## Testing

If your changes involve adding new features or modifying existing ones, make sure to add appropriate tests to cover the functionality. Run the existing tests to ensure that your changes do not break any existing functionality.

## Reporting Issues

If you encounter any issues or bugs, please report them by opening an issue in the GitHub repository. Provide detailed information about the problem, including steps to reproduce it.

## Pull Requests
When you are ready to submit, please create a pull request on GitHub. Please include a clear and concise description of what you have done and why you think it is useful to the project. If your contribution fixes a bug or implements a feature request, please link the relevant issue in your description.

## Review Process

Your pull request will be reviewed by the project [maintainers](https://github.com/Goodnessmbakara). They may provide feedback or request further changes. Once your changes are approved, they will be merged into the main project.

## License

By contributing to this project, you agree that your contributions will be licensed under the the [MIT License](https://mit-license.org/).
