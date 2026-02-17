# Data Model: Professional Modern Todo Frontend

## UI Components

### Card Component
- **Name**: TodoCard
- **Fields**:
  - id: string (unique identifier for the card)
  - title: string (todo title text)
  - description: string (optional todo description)
  - completed: boolean (completion status)
  - createdAt: datetime (creation timestamp)
  - updatedAt: datetime (last update timestamp)
- **Relationships**: Belongs to TodoList container
- **Validation**: Title must be 1-200 characters

### Button Component
- **Name**: ActionButton
- **Fields**:
  - type: string (primary, secondary, danger, success)
  - label: string (button text)
  - icon: string (optional icon class)
  - disabled: boolean (interaction state)
- **Relationships**: Associated with specific actions (add, edit, delete, complete)

### Form Component
- **Name**: TodoForm
- **Fields**:
  - title: string (required input field)
  - description: string (optional input field)
  - submitHandler: function (form submission callback)
- **Validation**: Title must be 1-200 characters

### Theme Configuration
- **Name**: ThemeSettings
- **Fields**:
  - mode: string ('light' or 'dark')
  - primaryColor: string (hex color code)
  - secondaryColor: string (hex color code)
  - fontFamily: string (font family name)
- **State Management**: Persisted in localStorage

## Layout Components

### Navigation Component
- **Name**: AppHeader
- **Fields**:
  - title: string (application title)
  - themeToggle: boolean (show theme switcher)
  - userMenu: boolean (show user menu if applicable)

### Container Component
- **Name**: TodoContainer
- **Fields**:
  - title: string (section title)
  - todos: array (list of TodoCard components)
  - isEmpty: boolean (empty state indicator)
- **Relationships**: Contains multiple TodoCard components

## Responsive Breakpoints

### Mobile
- **Breakpoint**: < 768px
- **Layout**: Single column, stacked elements
- **Components**: Collapsed navigation, touch-friendly buttons

### Tablet
- **Breakpoint**: 768px - 1024px
- **Layout**: 2-column grid for todo items
- **Components**: Moderate spacing, medium-sized elements

### Desktop
- **Breakpoint**: > 1024px
- **Layout**: Multi-column grid, sidebar navigation
- **Components**: Full-size elements, expanded controls