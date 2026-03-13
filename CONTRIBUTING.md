# 🤝 Contributing to UPI Fraud Detection

Thank you for your interest in contributing to the UPI Fraud Detection project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Areas for Contribution](#areas-for-contribution)

## 🤗 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Keep discussions professional

## 🚀 Getting Started

1. **Fork the repository**
   ```bash
   # Click 'Fork' on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/upi-fraud-detection.git
   cd upi-fraud-detection
   ```

3. **Set up development environment**
   ```bash
   # Follow SETUP.md instructions
   ./start_server.sh  # or start_server.bat on Windows
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Development Workflow

### Backend Development

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### ML Development

```bash
cd ml
# Modify training scripts
python retrain_model.py
```

## 📏 Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where applicable
- Write docstrings for functions
- Keep functions small and focused

**Example:**
```python
def extract_features(
    amount: float,
    time: str,
    receiver: str,
    account: str
) -> Dict[str, Any]:
    """
    Extract features for fraud detection.
    
    Args:
        amount: Transaction amount
        time: Transaction time (HH:MM format)
        receiver: Receiver UPI ID or name
        account: Sender account
    
    Returns:
        Dictionary of extracted features
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)

- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Keep components small and reusable

**Example:**
```jsx
const ResultCard = ({ result }) => {
  const isFraud = result.prediction === 'Fraud'
  
  return (
    <motion.div className="glass-card">
      {/* Component content */}
    </motion.div>
  )
}
```

### File Structure

- Keep related code together
- Use descriptive file names
- Maintain consistent naming conventions

## 🧪 Testing

### Backend Tests

```python
# backend/tests/test_prediction.py
import pytest
from app.utils.preprocessor import extract_features

def test_extract_time_features():
    features = extract_time_features("23:45")
    assert features["is_odd_hour"] == 1
    assert features["hour"] == 23
```

### Frontend Tests

```javascript
// frontend/src/__tests__/ManualInputForm.test.jsx
import { render, screen } from '@testing-library/react'
import ManualInputForm from '../components/ManualInputForm'

test('renders form inputs', () => {
  render(<ManualInputForm />)
  expect(screen.getByText('Manual Input')).toBeInTheDocument()
})
```

### Run Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 📝 Pull Request Process

1. **Update your branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout feature/your-feature
   git rebase main
   ```

2. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add feature description"
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature
   ```

4. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Provide clear description
   - Link related issues

### Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add support for multi-language SMS parsing
fix: Correct time feature extraction bug
docs: Update API documentation
refactor: Simplify prediction logic
```

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No console errors
- [ ] Screenshots added (if UI changes)

## 🎯 Areas for Contribution

### High Priority

1. **Enhanced SMS Parsing**
   - Support more bank formats
   - Multi-language support
   - Better regex patterns

2. **Improved ML Model**
   - Feature engineering
   - Model optimization
   - Ensemble methods

3. **Security Features**
   - Authentication system
   - Rate limiting
   - Input sanitization

4. **Testing**
   - Unit tests
   - Integration tests
   - E2E tests

### Medium Priority

1. **UI Enhancements**
   - Dark/Light mode toggle
   - More animations
   - Accessibility improvements

2. **Analytics Dashboard**
   - Fraud trends
   - Interactive charts
   - Export functionality

3. **Documentation**
   - Video tutorials
   - Code examples
   - Architecture diagrams

### Good First Issues

- Fix typos in documentation
- Add more example SMS formats
- Improve error messages
- Add loading states
- Enhance mobile responsiveness

## 🐛 Bug Reports

### Before Reporting

- Check existing issues
- Verify it's reproducible
- Test with latest version

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 120]
- Python version:
- Node version:

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Any other relevant information
```

## 🔍 Code Review Process

### As a Reviewer

- Be constructive and respectful
- Explain the "why" behind suggestions
- Approve if no blocking issues
- Test the changes locally

### As a Contributor

- Respond to feedback promptly
- Ask questions if unclear
- Make requested changes
- Thank reviewers

## 📚 Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [React Documentation](https://react.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows)

## 🎓 Learning Path

New to the project? Here's a suggested learning path:

1. **Week 1**: Explore the codebase
   - Run the application
   - Read documentation
   - Understand architecture

2. **Week 2**: Make small changes
   - Fix documentation
   - Add comments
   - Improve error messages

3. **Week 3**: Tackle bigger issues
   - Bug fixes
   - Small features
   - Tests

4. **Week 4+**: Major contributions
   - New features
   - Architecture improvements
   - Performance optimizations

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## 📞 Getting Help

- Open a GitHub issue
- Check existing documentation
- Ask in discussions

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to UPI Fraud Detection! 🛡️**

