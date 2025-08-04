# Seedling Template Test Checklist ✅

> **Purpose**: Comprehensive testing checklist for the Seedling Copier template to ensure all components work correctly when generating new projects.

---

## 📋 Legend

| Symbol | Meaning |
| ------ | ------- |
| ☐ | Test **not** completed |
| 🛠 | Test **in progress** |
| ✅ | Test **passed / verified** |
| ❌ | Test **failed** |

---

## 1. Template Generation

### 1.1 Basic Template Generation
- ✅ **Generate project from template**: `copier copy . /tmp/seedling-test --trust`
- ✅ **Verify all files are created**: Check that all template files are properly generated
- ✅ **Verify Jinja variables are replaced**: Ensure `{{ project_slug }}` etc. are replaced with actual values
- ✅ **Verify post-generation tasks run**: git init, pre-commit install, uv lock

### 1.2 Template Configuration
- ✅ **Verify copier.yml questions work**: All prompts appear and accept input
- ✅ **Verify conditional paths work**: Files with conditional logic are included/excluded correctly
- ✅ **Verify default values work**: Template generates with sensible defaults

---

## 2. Pre-commit Ecosystem

### 2.1 Pre-commit Installation
- ✅ **Pre-commit installs correctly**: `pre-commit install` runs without errors
- ✅ **Git hooks are created**: `.git/hooks/pre-commit` exists and is executable

### 2.2 Pre-commit Hook Testing
- ✅ **Black formatting works**: Code formatting passes without any fixes needed
- ✅ **Ruff linting works**: Code linting passes successfully
- ✅ **Yesqa works**: Unused noqa comments are stripped
- ✅ **MyPy type checking passes**: Type checking passes without any errors
- ✅ **Standard hooks work**: File checks, formatting, etc. all function
- ✅ **Commitizen configured**: Commit message validation is set up
- ✅ **CI autoupdate configured**: Weekly schedule is set

### 2.3 Tool Versions
- ✅ **Black 25.1.0**: Latest version is used
- ✅ **Ruff v0.12.7**: Latest version is used
- ✅ **MyPy 1.17.1**: Latest version is used
- ✅ **Yesqa v1.5.0**: Latest version is used
- ✅ **Commitizen v4.8.3**: Latest version is used

---

## 3. Project Structure

### 3.1 Directory Structure
- ✅ **src/{{ project_slug }}/**: Main package directory exists
- ✅ **tests/unit/**: Unit tests directory exists
- ✅ **tests/integration/**: Integration tests directory exists
- ✅ **tests/e2e/**: End-to-end tests directory exists
- ✅ **docs/**: Documentation directory exists
- ✅ **examples/**: Examples directory exists (empty placeholder)

### 3.2 Key Files
- ✅ **pyproject.toml**: Project configuration with correct dependencies
- ✅ **.pre-commit-config.yaml**: Pre-commit configuration with latest versions
- ✅ **noxfile.py**: Nox sessions for development tasks
- ✅ **README.md**: Project documentation
- ✅ **LICENSE**: MIT license (or selected license)
- ✅ **.gitignore**: Appropriate git ignore rules

---

## 4. Dependencies and Environment

### 4.1 Package Management
- ✅ **uv.lock generated**: Lock file is created with correct Python version
- ✅ **Virtual environment works**: `.venv` directory is created
- ✅ **Dependencies install**: `uv add` and `uv install` work correctly

### 4.2 Development Dependencies
- ✅ **Black available**: `uv run black --version` works
- ✅ **Ruff available**: `uv run ruff --version` works
- ✅ **MyPy available**: `uv run mypy --version` works
- ✅ **Pre-commit available**: `uv run pre-commit --version` works

---

## 5. Template Configuration Files

### 5.1 Copier Configuration
- ✅ **copier.yml exists**: Template configuration is present
- ✅ **Questions defined**: All required questions are configured
- ✅ **Validators work**: Regex validators function correctly
- ✅ **Conditional paths work**: Jinja conditionals function correctly

### 5.2 Template Files
- ✅ **Jinja templates exist**: All `.jinja` files are present
- ✅ **Template variables work**: `{{ project_slug }}` etc. are replaced
- ✅ **Conditional content works**: Content based on user choices is included/excluded

---

## 6. Documentation and Metadata

### 6.1 Project Metadata
- ✅ **Project name**: Correctly set from user input
- ✅ **Author information**: Correctly set from user input
- ✅ **Version**: Correctly set from user input
- ✅ **Description**: Correctly set from user input
- ✅ **License**: Correctly set from user input

### 6.2 Documentation
- ✅ **README.md**: Contains project information and setup instructions
- ✅ **CONTRIBUTING.md**: Contains contribution guidelines
- ✅ **SECURITY.md**: Contains security policy
- ✅ **LICENSE**: Contains appropriate license text

---

## 7. Development Workflow

### 7.1 Git Setup
- ✅ **Git repository initialized**: `git init` runs successfully
- ✅ **Initial commit possible**: Can make first commit
- ✅ **Branch protection ready**: Repository is ready for branch protection rules

### 7.2 Development Tools
- ✅ **Pre-commit hooks work**: All hooks run without errors
- ✅ **Code formatting works**: Black and Ruff format code correctly
- ✅ **Type checking works**: MyPy runs and reports issues
- ✅ **Testing framework ready**: pytest configuration is present

---

## 8. Template Quality

### 8.1 Code Quality
- ✅ **Template code is clean**: No linting errors in template files
- ✅ **Generated code is clean**: Generated projects pass all linting checks immediately
- ✅ **No hardcoded values**: All project-specific values use Jinja variables
- ✅ **Perfect greenfield experience**: All pre-commit hooks pass without any fixes needed

### 8.2 Template Completeness
- ✅ **All required files present**: No missing essential files
- ✅ **No unnecessary files**: No template artifacts in generated projects
- ✅ **Consistent structure**: All generated projects have same structure

---

## 9. Edge Cases and Error Handling

### 9.1 Template Generation Errors
- ☐ **Invalid project names**: Test with invalid characters
- ☐ **Empty values**: Test with empty inputs
- ☐ **Special characters**: Test with special characters in names
- ☐ **Long names**: Test with very long project names

### 9.2 Dependency Issues
- ☐ **Missing dependencies**: Test behavior when dependencies fail to install
- ☐ **Version conflicts**: Test with conflicting dependency versions
- ☐ **Network issues**: Test behavior with poor network connectivity

---

## 10. Integration Testing

### 10.1 GitHub Integration
- ☐ **GitHub repository creation**: Test creating repo from generated project
- ☐ **GitHub Actions workflows**: Test that workflows are properly configured
- ☐ **Branch protection**: Test setting up branch protection rules

### 10.2 CI/CD Pipeline
- ☐ **Pre-commit CI**: Test pre-commit-ci integration
- ☐ **CodeQL**: Test security scanning setup
- ☐ **Coverage reporting**: Test code coverage integration

---

## 11. User Experience

### 11.1 Template Usage
- ☐ **Clear prompts**: Questions are clear and understandable
- ☐ **Helpful defaults**: Default values are sensible
- ☐ **Error messages**: Error messages are helpful
- ☐ **Documentation**: Template usage is well documented

### 11.2 Generated Project Experience
- ☐ **Easy setup**: Generated project is easy to get started with
- ☐ **Clear documentation**: README provides clear next steps
- ☐ **Working examples**: Example code works out of the box
- ☐ **Development workflow**: Development process is smooth

---

*Last updated: 2025-01-04*
*Template version: 0.1.0*
