# Contributing to AfsGbindView

Thank you for your interest in contributing to AfsGbindView! This document provides guidelines and information for contributors.

## 🤝 Ways to Contribute

- **Bug Reports**: Report issues or unexpected behavior
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit bug fixes or new features
- **Documentation**: Improve documentation and examples
- **Testing**: Help test the application with different datasets

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic knowledge of Python and Streamlit

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/AfsGbindView.git
   cd AfsGbindView
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   streamlit run mmgbsa_ui_v2.py
   ```

## 📝 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/) for Python code style
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example:

```python
def calculate_running_mean(data: pd.Series, window_size: int) -> pd.Series:
    """
    Calculate running mean for a pandas Series.
    
    Args:
        data: Input data series
        window_size: Size of the rolling window
        
    Returns:
        Series with running mean values
    """
    return data.rolling(window=window_size, min_periods=1).mean()
```

### Streamlit Code Style

- Organize UI elements logically
- Use clear labels and help text
- Handle errors gracefully with user-friendly messages
- Use session state appropriately for persistent data

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details**:
   - Operating system
   - Python version
   - Streamlit version
   - Browser (if applicable)
5. **Sample data** (if possible) or data format details
6. **Screenshots** (if relevant)

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Upload file '....'
4. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
 - Python Version: [e.g. 3.9.7]
 - Streamlit Version: [e.g. 1.28.0]
 - Browser: [e.g. Chrome 91.0]

**Additional Context**
Add any other context about the problem here.
```

## 💡 Feature Requests

When suggesting features:

1. **Describe the problem** you're trying to solve
2. **Explain the proposed solution**
3. **Consider alternatives** you've thought about
4. **Provide use cases** or examples

## 🔧 Development Guidelines

### Branching Strategy

- `main`: Stable release branch
- `develop`: Development branch for new features
- Feature branches: `feature/your-feature-name`
- Bug fixes: `fix/bug-description`

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add error bar customization options
fix: resolve legend positioning issue
docs: update installation instructions
style: improve code formatting
test: add unit tests for statistics functions
```

### Pull Request Process

1. **Create a feature branch** from `develop`
2. **Make your changes** following the style guidelines
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** to the `develop` branch

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have tested these changes locally
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Screenshots (if applicable)
Add screenshots to demonstrate the changes

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

## 🧪 Testing

### Manual Testing

Before submitting changes:

1. **Test basic functionality**:
   - File upload and parsing
   - Plot generation
   - Settings persistence
   - Export functionality

2. **Test edge cases**:
   - Empty files
   - Large datasets
   - Invalid data formats
   - Different ligand names

3. **Test UI/UX**:
   - Responsive design
   - Error messages
   - Loading states
   - Browser compatibility

### Automated Testing

We encourage adding unit tests for new functionality:

```python
import pytest
import pandas as pd
from your_module import calculate_running_mean

def test_running_mean_calculation():
    """Test running mean calculation with known values."""
    data = pd.Series([1, 2, 3, 4, 5])
    result = calculate_running_mean(data, window_size=3)
    expected = pd.Series([1.0, 1.5, 2.0, 3.0, 4.0])
    pd.testing.assert_series_equal(result, expected)
```

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include parameter descriptions and return values
- Provide usage examples where helpful

### User Documentation

- Update README.md for new features
- Add examples for complex functionality
- Include screenshots for UI changes

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Python Style Guide (PEP 8)](https://pep8.org/)

## 📞 Questions?

If you have questions about contributing:

- Check existing [Issues](https://github.com/yourusername/AfsGbindView/issues)
- Start a [Discussion](https://github.com/yourusername/AfsGbindView/discussions)
- Contact the maintainers

## 🎉 Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for helping make AfsGbindView better for the computational chemistry community! 🧬 