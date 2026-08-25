---
title: Senior Frontend Developer Guide
tags: [programming, guide]
status: stable
---

# Senior Frontend Developer Best Practices Guide

A comprehensive guide to the patterns, principles, and practices that separate senior frontend developers from the rest.

---

## Table of Contents

1. [The Architecture Layer](#the-architecture-layer)
2. [Component Architecture](#component-architecture)
3. [Code Organization](#code-organization)
4. [The Component Layer](#the-component-layer)
5. [Performance Optimization](#performance-optimization)
6. [Testing Strategy](#testing-strategy)
7. [Code Quality](#code-quality)
8. [Error Handling](#error-handling)
9. [Type Safety](#type-safety)
10. [Accessibility](#accessibility)
11. [Development Experience](#development-experience)

---

## The Architecture Layer

### Thinking in Systems

When you open a codebase written by a Senior Frontend developer, you immediately sense something different. The code doesn't just work—it feels purposeful. The choices are deliberate, and the patterns feel intentional. This difference comes from understanding not just what to do, but **why it matters**.

The journey from junior to senior isn't about cramming more JavaScript syntax or memorizing API methods. It's about learning the principles of solid Frontend architecture and applying them consistently, even when shortcuts would be easier.

### State Architecture: Beyond "Just Put It in State"

One of the most common habits in early React development is treating all state the same way. A toggle, a text input, an API response, a set of filters—everything goes into the same bucket of "state."

In smaller apps, this works fine. But as your app grows, boundaries blur, complexity creeps in, and managing state becomes harder than necessary.

**Experienced developers classify state into layers, each belonging to a natural part of the system:**

#### 1. Server State
Server state belongs in libraries like **React Query**, **SWR**, or **Apollo**. This isn't only about caching data.

Server state has unique characteristics:
- It can become stale
- It must stay in sync with the backend
- It's often shared across multiple parts of the app

Trying to manage it with `useState` is technically possible, but it won't be a good fit. An analogy: trying to carve wood with a butter knife.

```javascript
// Junior approach - treating server data like local state
const [users, setUsers] = useState([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);

// Senior approach - recognizing server state
const { data: users, isLoading, error } = useQuery('users', fetchUsers);
```

#### 2. Global Client State
Global client state should live in context providers, **Zustand**, or **Redux**—but only when it *needs* to be global.

**Common mistake:** Projects where every piece of state gets lifted into a global store "just in case." This only adds weight. It creates:
- Unnecessary coupling
- Less portable components
- Complicated testing
- Over-engineering

Global state is powerful, but like any powerful tool, it should be used carefully.

#### 3. Local Component State
Local component state belongs in `useState` or `useReducer` when it's scoped to a single component and maybe its immediate children.

Examples:
- A modal's open/close flag
- A form's current values
- A spinner showing while a component is doing its work

These don't need to escape the component. Keeping them local:
- Reduces noise in the bigger picture
- Keeps your mental model simpler
- Makes components more reusable

#### 4. URL State
URL state is best handled through the router whenever the state directly affects what the user sees on screen.

Examples:
- Filters
- Pagination
- Selected tabs

**The key insight:** If refreshing the page should preserve it, that's a clear sign it belongs in the URL.

This practice:
- Aligns with how browsers naturally work
- Gives users the ability to share, bookmark, and return to the exact same view
- Improves user experience significantly

#### State Architecture Summary

By treating state as layers—server, global, local, and URL—you reduce accidental complexity. Each kind of state has a natural home, which makes the application easier to extend, debug, and reason about over time.

---

## Component Architecture

### The Art of Boundaries

We often hear about "separation of concerns," but what does that actually look like in a React application? Senior developers think in terms of **Component Boundaries**—not just breaking things into smaller pieces, but creating the *right* boundaries.

### Container vs. Presentational Pattern

This pattern isn't dead, despite what some may claim. It has evolved, but the core insight remains valuable:

**Components that know about business logic shouldn't also be responsible for styling and layout details. Components that handle styling and interaction shouldn't need to understand your API structure.**

#### Bad Example: Mixed Responsibilities
```javascript
// Harder to test and reuse
const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [editing, setEditing] = useState(false);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  
  const handleSave = async (data) => {
    await updateUser(userId, data);
    setUser(data);
    setEditing(false);
  };
  
  return (
    <div className="user-profile bg-white shadow-lg rounded-lg p-6">
      {editing ? (
        <UserEditForm user={user} onSave={handleSave} />
      ) : (
        <UserDisplay user={user} onEdit={() => setEditing(true)} />
      )}
    </div>
  );
};
```

#### Good Example: Clear Separation
```javascript
// Container component - handles business logic
const UserProfileContainer = ({ userId }) => {
  const { data: user } = useQuery(['user', userId], () => fetchUser(userId));
  const updateMutation = useMutation(updateUser);
  
  const handleSave = (data) => {
    updateMutation.mutate({ userId, data });
  };
  
  return <UserProfile user={user} onSave={handleSave} />;
};

// Presentational component - handles styling and display
const UserProfile = ({ user, onSave }) => {
  const [editing, setEditing] = useState(false);
  
  return (
    <Card>
      {editing ? (
        <UserEditForm user={user} onSave={onSave} />
      ) : (
        <UserDisplay user={user} onEdit={() => setEditing(true)} />
      )}
    </Card>
  );
};
```

**Benefits:**
- Easier to test each piece separately
- Presentational components are reusable
- Business logic is centralized
- Clearer responsibility for each component

### Custom Hooks for Logic Extraction

Custom hooks are one of the most powerful tools for sharing stateful logic between components.

**The principle:** When the same pattern of state or behavior shows up in multiple places, it's a sign to extract that logic into a hook.

But extraction alone isn't enough. A well-crafted custom hook has a thoughtful API—it should feel as intuitive and natural to use as React's built-in hooks like `useState` or `useEffect`.

#### Example: Custom useToggle Hook
```javascript
// Not just extracting logic, but designing a clean API
const useToggle = (initialValue = false) => {
  const [value, setValue] = useState(initialValue);
  
  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);
  
  return [value, { toggle, setTrue, setFalse, setValue }];
};

// Usage feels natural and expressive
const [isModalOpen, { toggle: toggleModal, setTrue: openModal }] = useToggle();
```

**Best Practices for Custom Hooks:**
- Return a clean, intuitive API
- Document expected behavior
- Keep hooks focused on one responsibility
- Make them easy to test
- Consider performance implications

---

## Code Organization

### Feature-Based Directory Structure

Organizing files by type (components, hooks, utilities) works fine when projects are small. As your application grows, this structure eventually falls apart.

When you're focused on a feature like user profiles, hunting through multiple folders to find all related files is inefficient.

#### Senior Approach: Feature-Based Organization

A feature-based directory structure groups everything related to a specific feature in one place. Components, hooks, styles, and tests live side-by-side.

```
src/
  features/
    auth/
      components/
        LoginForm.jsx
        SignupForm.jsx
      hooks/
        useAuth.js
      services/
        authApi.js
      index.js
    userProfile/
      components/
        UserProfile.jsx
        UserEditForm.jsx
      hooks/
        useUserProfile.js
      services/
        userApi.js
      index.js
    dashboard/
      components/
        Dashboard.jsx
        DashboardCard.jsx
      hooks/
        useDashboardData.js
      index.js
  shared/
    components/
      Button/
      Modal/
      Card/
    hooks/
      useLocalStorage.js
      usePrevious.js
    utils/
      formatters.js
      validators.js
    constants/
      config.js
  App.jsx
  index.js
```

**Benefits:**
- Each feature becomes a mini-application with its own concerns
- Locality of reference—related code lives close together
- Easier to understand, update, and test
- Scales better as your application grows
- Simpler to maintain and extend

### Export Strategies That Scale

Export strategies might seem like a small detail, but they have a real impact on bundle size and developer experience.

Senior developers pay attention to how components are exported and imported because it influences the shape of the import graph.

#### Barrel Exports for Clean Imports
```javascript
// features/userProfile/index.js
// Barrel exports with re-exports for clean imports
export { UserProfile } from './components/UserProfile';
export { UserEditForm } from './components/UserEditForm';
export { useUserProfile } from './hooks/useUserProfile';

// This way, other modules can import like:
import { UserProfile, useUserProfile } from 'features/userProfile';

// Instead of:
import { UserProfile } from 'features/userProfile/components/UserProfile';

// Some components are meant for internal use only:
import { UserProfileHeader } from './components/UserProfileHeader';
// Purposefully not exported from the barrel
```

#### Tree Shaking Optimization

Understand **tree shaking** and structure your exports to make it work effectively.

```javascript
// Bad for tree shaking - bundled into a default object
export default {
  formatCurrency,
  formatDate,
  formatPhone
};

// Good for tree shaking - individual exports
export const formatCurrency = (amount) => { /* */ };
export const formatDate = (date) => { /* */ };
export const formatPhone = (phone) => { /* */ };
```

When using individual exports, bundlers can eliminate unused functions, resulting in smaller bundle sizes.

---

## The Component Layer

### JSX: The Art of Readable Templates

Writing clean JSX isn't about following arbitrary rules. It's about making the structure and purpose of a component immediately clear to anyone reading it.

**Goal:** When a developer glances at JSX, they should easily understand what the component does without untangling complex inline logic.

### Avoid Inline Anonymous Functions

While React handles these quite well now, avoid them not for performance reasons, but because they:
- Hurt readability
- Make debugging more difficult

Clear, named functions improve both code clarity and the developer experience.

#### Cluttered and Hard to Debug
```javascript
<Button
  onClick={(e) => {
    e.preventDefault();
    if (user.permissions.includes('delete')) {
      setConfirmDialogOpen(true);
    } else {
      showError('Insufficient permissions');
    }
  }}
>
  Delete
</Button>
```

#### Clear Intent, Easy to Debug
```javascript
const handleDeleteClick = (e) => {
  e.preventDefault();
  if (user.permissions.includes('delete')) {
    setConfirmDialogOpen(true);
  } else {
    showError('Insufficient permissions');
  }
};

<Button onClick={handleDeleteClick}>Delete</Button>
```

### Fragment Usage

Shows attention to semantic HTML structure.

```javascript
// Creates unnecessary div wrapper
const UserInfo = ({ user }) => (
  <div>
    <h2>{user.name}</h2>
    <p>{user.email}</p>
  </div>
);

// Respects HTML structure
const UserInfo = ({ user }) => (
  <>
    <h2>{user.name}</h2>
    <p>{user.email}</p>
  </>
);
```

### Props: The Component's API

Props are essentially a component's public API. They deserve the same thoughtful design and care you give any public interface.

This means:
- Considering developer experience
- Ensuring type safety
- Building for extensibility from the start

#### Prop Destructuring with Defaults

This approach makes your components self-documenting. Anyone reading the code can quickly see what props the component expects and what defaults they fall back on.

```javascript
// Hard to understand component requirements
const Button = (props) => {
  const size = props.size || 'medium';
  const variant = props.variant || 'primary';
  // ...
};

// Clear component API
const Button = ({
  children,
  size = 'medium',
  variant = 'primary',
  disabled = false,
  onClick,
  ...rest
}) => {
  // ...
};
```

#### Prop Validation with PropTypes

Isn't just about catching bugs—it's about documenting expected usage:

```javascript
Button.propTypes = {
  children: PropTypes.node.isRequired,
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger']),
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
};
```

#### Compound Components

For complex UI patterns that need to work together:

```javascript
// Instead of a monolithic Modal with tons of props
<Modal
  title="Confirm Delete"
  content="Are you sure?"
  primaryButton="Delete"
  secondaryButton="Cancel"
  onPrimaryClick={handleDelete}
  onSecondaryClick={handleCancel}
/>

// Compound components provide flexibility and clarity
<Modal isOpen={isModalOpen} onClose={handleClose}>
  <Modal.Header>
    <Modal.Title>Confirm Delete</Modal.Title>
  </Modal.Header>
  <Modal.Body>
    <p>Are you sure you want to delete this item?</p>
  </Modal.Body>
  <Modal.Footer>
    <Button variant="danger" onClick={handleDelete}>Delete</Button>
    <Button variant="secondary" onClick={handleCancel}>Cancel</Button>
  </Modal.Footer>
</Modal>
```

**Benefits of Compound Components:**
- Flexibility in structure
- Clear relationship between parts
- Easy to extend
- More readable and maintainable

---

## Performance Optimization

### Performance with Purpose

Performance optimization isn't about tweaking for the sake of it. Every optimization brings tradeoffs—you might gain speed at the cost of added complexity, reduced readability, or a bigger bundle.

**The most experienced Frontend developers start by measuring.** They make sure improvements really matter before changing anything.

### React DevTools Profiler

This is your go-to tool. It helps spot:
- Components that re-render more often than they should
- Expensive renders that block the main thread
- Unnecessary work happening in child components

This investigation lets you focus efforts where they'll have real impact.

### useMemo and useCallback: Options, Not Must-Haves

The goal isn't to sprinkle them everywhere, but to use them when profiling shows a real benefit.

```javascript
// Don't memoize everything
const ExpensiveComponent = ({ data, filter }) => {
  // This is fine - simple string operations are cheap
  const title = data.name.toUpperCase();
  
  // This warrants memoization - expensive computation
  const processedData = useMemo(() => {
    return data.items
      .filter(item => item.category === filter)
      .map(item => ({
        ...item,
        score: calculateComplexScore(item)
      }))
      .sort((a, b) => b.score - a.score);
  }, [data.items, filter]);
  
  return (
    <div>
      <h1>{title}</h1>
      <DataList items={processedData} />
    </div>
  );
};
```

### React.memo for Memoized Components

Memoize components that receive the same props frequently:

```javascript
// Memoize components that receive stable props but parent re-renders often
const UserListItem = React.memo(({ user, onSelect }) => (
  <div onClick={() => onSelect(user.id)}>
    <img src={user.avatar} alt={user.name} />
    <span>{user.name}</span>
  </div>
));

// Ensure handlers are stable too
const UserList = ({ users }) => {
  const handleUserSelect = useCallback((userId) => {
    // handle selection
  }, []);
  
  return (
    <div>
      {users.map(user => (
        <UserListItem
          key={user.id}
          user={user}
          onSelect={handleUserSelect}
        />
      ))}
    </div>
  );
};
```

### Bundle Optimization

Think about the **loading experience** as part of the user interface. A fast, progressive loading experience is often more important than shaving milliseconds off runtime performance.

#### Code Splitting at Feature Boundaries
```javascript
// Route-level splitting
const UserProfile = lazy(() => import('../features/userProfile'));
const AdminPanel = lazy(() => import('../features/admin'));

// Component-level splitting for large features
const AdvancedCharts = lazy(() => import('./AdvancedCharts'));

const Dashboard = () => {
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  return (
    <div>
      <BasicStats />
      {showAdvanced && (
        <Suspense fallback={<ChartSkeleton />}>
          <AdvancedCharts />
        </Suspense>
      )}
    </div>
  );
};
```

#### Dynamic Imports for Heavy Libraries
```javascript
// Only load heavy date manipulation library when needed
const handleDateRangeSelect = async (startDate, endDate) => {
  const { formatDateRange } = await import('date-fns');
  return formatDateRange(startDate, endDate);
};
```

---

## Testing Strategy

### The Testing Pyramid

A solid testing strategy usually looks like a pyramid:

- **Base:** Plenty of unit tests for small pieces of logic
- **Middle:** A smaller set of integration tests for component interaction
- **Top:** End-to-end tests for the most important user flows

This approach balances coverage with maintenance effort.

### Unit Testing Custom Hooks

```javascript
import { renderHook, act } from '@testing-library/react';
import { useToggle } from './useToggle';

describe('useToggle', () => {
  it('should initialize with provided value', () => {
    const { result } = renderHook(() => useToggle(true));
    expect(result.current[0]).toBe(true);
  });
  
  it('should toggle value', () => {
    const { result } = renderHook(() => useToggle(false));
  
    act(() => {
      result.current[1].toggle();
    });
  
    expect(result.current[0]).toBe(true);
  });
});
```

### Component Testing: Focus on Behavior

Test behavior, not implementation details:

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  const mockUser = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com'
  };
  
  it('should allow editing when edit button is clicked', () => {
    render(<UserProfile user={mockUser} onSave={jest.fn()} />);
  
    // Test user behavior, not implementation details
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
  
    expect(screen.getByDisplayValue(mockUser.name)).toBeInTheDocument();
    expect(screen.getByDisplayValue(mockUser.email)).toBeInTheDocument();
  });
});
```

### Integration Testing

Test complex component interactions:

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { UserProfileContainer } from './UserProfileContainer';
import * as userApi from './userApi';

jest.mock('./userApi');

describe('UserProfileContainer', () => {
  it('should save user changes', async () => {
    const mockUser = { id: '1', name: 'John', email: 'john@test.com' };
    userApi.fetchUser.mockResolvedValue(mockUser);
    userApi.updateUser.mockResolvedValue({ ...mockUser, name: 'Jane' });
  
    const queryClient = new QueryClient();
    render(
      <QueryClientProvider client={queryClient}>
        <UserProfileContainer userId="1" />
      </QueryClientProvider>
    );
  
    // Wait for user to load
    await screen.findByText(mockUser.name);
  
    // Edit and save
    fireEvent.click(screen.getByRole('button', { name: /edit/i }));
    fireEvent.change(screen.getByDisplayValue(mockUser.name), {
      target: { value: 'Jane' }
    });
    fireEvent.click(screen.getByRole('button', { name: /save/i }));
  
    await waitFor(() => {
      expect(userApi.updateUser).toHaveBeenCalledWith('1', {
        ...mockUser,
        name: 'Jane'
      });
    });
  });
});
```

---

## Code Quality

### Naming: The Foundation of Readability

Good naming is less about strict conventions and more about making code easier to read and understand.

Every time someone reads your code, they shouldn't have to decipher abbreviations or guess what something is supposed to do. A clear, descriptive name keeps everyone on the same page and lowers the mental effort needed to work in the codebase.

#### Component Naming

Use PascalCase names that make it obvious what the component represents or does:

```javascript
// Vague and generic
const Panel = () => { /* */ };
const Form = () => { /* */ };

// Clear and specific
const UserProfilePanel = () => { /* */ };
const LoginForm = () => { /* */ };
const ProductSearchForm = () => { /* */ };
```

#### Functions and Variables

Use camelCase and action-oriented names:

```javascript
// What does this function do?
const process = (data) => { /* */ };
const calc = (x, y) => { /* */ };

// Clear intent
const validateUserInput = (data) => { /* */ };
const calculateMonthlyPayment = (principal, rate) => { /* */ };
```

#### Boolean Variables and Functions

Start with verbs that imply true/false:

```javascript
// Confusing
const user = true;
const modal = false;

// Clear
const isUserLoggedIn = true;
const shouldShowModal = false;
const hasPermission = (user, action) => { /* */ };
const canEditProfile = (user) => { /* */ };
```

#### Event Handlers

Follow consistent patterns:

```javascript
// Inconsistent naming
const click = () => { /* */ };
const userSubmit = () => { /* */ };
const changing = () => { /* */ };

// Consistent patterns
const handleClick = () => { /* */ };
const handleUserSubmit = () => { /* */ };
const handleInputChange = () => { /* */ };
```

---

## Error Handling

### Building Applications That Fail Gracefully

Users shouldn't be faced with white screens or broken features just because of network hiccups, API changes, or unexpected data formats.

### Error Boundaries

Error boundaries are key to isolating errors at the component level. They let us catch rendering errors in specific parts of the UI and show fallback content, preventing the entire app from crashing.

```javascript
class FeatureErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Log to monitoring service
    logError(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <ErrorFallback
          error={this.state.error}
          retry={() => this.setState({ hasError: false, error: null })}
        />
      );
    }
  
    return this.props.children;
  }
}

// Wrap features, not the entire app
<FeatureErrorBoundary>
  <UserProfile />
</FeatureErrorBoundary>
```

### Defensive Programming for External Data

```javascript
// Assumes perfect data structure
const UserCard = ({ user }) => (
  <div>
    <img src={user.profile.avatar.url} alt={user.name} />
    <h3>{user.name}</h3>
    <p>{user.profile.bio}</p>
  </div>
);

// Handles imperfect data gracefully
const UserCard = ({ user }) => {
  const avatarUrl = user?.profile?.avatar?.url;
  const bio = user?.profile?.bio;
  
  return (
    <div>
      {avatarUrl && (
        <img src={avatarUrl} alt={user?.name || 'User'} />
      )}
      <h3>{user?.name || 'Unknown User'}</h3>
      {bio && <p>{bio}</p>}
    </div>
  );
};
```

### Loading and Error States as First-Class UI Concerns

```javascript
const UserProfile = ({ userId }) => {
  const { data: user, isLoading, error } = useQuery(
    ['user', userId],
    () => fetchUser(userId)
  );
  
  if (isLoading) {
    return <UserProfileSkeleton />;
  }
  
  if (error) {
    return (
      <ErrorCard
        title="Unable to load profile"
        message="Please try again in a moment"
        onRetry={() => queryClient.invalidateQueries(['user', userId])}
      />
    );
  }
  
  if (!user) {
    return (
      <EmptyState
        title="User not found"
        message="This user profile doesn't exist or has been removed"
      />
    );
  }
  
  return <UserProfileContent user={user} />;
};
```

---

## Type Safety

### TypeScript: Catching Errors at Compile Time

Whether it's TypeScript or PropTypes, type safety is more than just preventing bugs. It's a way to communicate clearly.

Types serve as documentation for assumptions and help catch inconsistencies before they make it into production.

### Designing Expressive TypeScript Interfaces

Focus on expressing intent clearly. Well-crafted types make it easier for everyone to understand how data flows through the app:

```typescript
// Basic but incomplete
interface User {
  id: string;
  name: string;
  email: string;
}

// Expressive and comprehensive
interface User {
  readonly id: string;
  name: string;
  email: string;
  profile?: {
    avatar?: {
      url: string;
      alt?: string;
    };
    bio?: string;
    location?: string;
  };
  permissions: readonly Permission[];
  status: 'active' | 'suspended' | 'pending';
  createdAt: Date;
  lastLoginAt: Date | null;
}

// Component props that express relationships
interface UserProfileProps {
  user: User;
  currentUser?: User;
  onEdit?: () => void;
  onDelete?: () => void;
  // Make relationships explicit
  canEdit?: boolean;
  canDelete?: boolean;
}
```

### Generic Types for Reusable Patterns

```typescript
// Reusable async state pattern
interface AsyncData<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

// API response wrapper
interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
  message?: string;
  pagination?: {
    page: number;
    totalPages: number;
    totalItems: number;
  };
}

// Generic hook for async data
const useAsyncData = <T>(
  fetcher: () => Promise<T>,
  deps: React.DependencyList = []
): AsyncData<T> => {
  // Implementation
};
```

---

## Accessibility

### Building for Everyone

Accessibility isn't an afterthought—it's a core part of building quality software.

### Semantic HTML as Foundation

Accessibility begins with using semantic HTML correctly. When the right elements are chosen, many accessibility features come built in:
- Keyboard navigation
- Screen reader support
- Automatic focus management

Choosing between a `<button>` and a `<div>` is more than semantics. It directly impacts how users with assistive technologies experience your app.

#### Interactive Elements

```javascript
// Looks like a button, doesn't work like one
<div className="button" onClick={handleClick}>
  Click me
</div>

// Works for everyone
<button type="button" onClick={handleClick}>
  Click me
</button>
```

### Form Labels and Structure

```javascript
// Inaccessible form
<form>
  <input type="text" placeholder="Enter your name" />
  <input type="email" placeholder="Enter your email" />
  <button>Submit</button>
</form>

// Accessible form
<form>
  <div>
    <label htmlFor="name">Name</label>
    <input
      id="name"
      type="text"
      placeholder="Enter your name"
      required
      aria-describedby="name-help"
    />
    <div id="name-help">This will be displayed on your profile</div>
  </div>
  
  <div>
    <label htmlFor="email">Email</label>
    <input
      id="email"
      type="email"
      placeholder="Enter your email"
      required
      aria-describedby="email-help"
    />
    <div id="email-help">We'll never share your email</div>
  </div>
  
  <button type="submit">Submit</button>
</form>
```

### ARIA Attributes When HTML Isn't Enough

```javascript
const ToggleButton = ({ pressed, onToggle, children }) => (
  <button
    type="button"
    aria-pressed={pressed}
    onClick={onToggle}
    className={pressed ? 'button-pressed' : 'button-normal'}
  >
    {children}
  </button>
);

const Modal = ({ isOpen, onClose, title, children }) => (
  <>
    {isOpen && <div className="modal-backdrop" onClick={onClose} />}
    <div
      className={`modal ${isOpen ? 'modal-open' : 'modal-hidden'}`}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="modal-header">
        <h2 id="modal-title">{title}</h2>
        <button
          type="button"
          aria-label="Close modal"
          onClick={onClose}
        >
          ×
        </button>
      </div>
      <div className="modal-content">
        {children}
      </div>
    </div>
  </>
);
```

### Keyboard Navigation and Focus Management

Building interactions that work well with keyboards—not just mice or touch—is essential. This means:
- Carefully managing focus
- Offering skip links to help users bypass repeated content
- Ensuring all interactive elements can be reached using the keyboard alone

#### Focus Management in Modals

```javascript
const Modal = ({ isOpen, onClose, children }) => {
  const modalRef = useRef();
  
  useEffect(() => {
    if (isOpen) {
      const previousFocus = document.activeElement;
  
      // Focus first focusable element in modal
      const firstFocusable = modalRef.current?.querySelector(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      firstFocusable?.focus();
  
      // Return focus when modal closes
      return () => {
        previousFocus?.focus();
      };
    }
  }, [isOpen]);
  
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };
  
  if (!isOpen) return null;
  
  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      onKeyDown={handleKeyDown}
      className="modal"
    >
      {children}
    </div>
  );
};
```

#### Custom Focus Trap Hook

```javascript
const useFocusTrap = (isActive) => {
  const containerRef = useRef();
  
  useEffect(() => {
    if (!isActive) return;
  
    const container = containerRef.current;
    if (!container) return;
  
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
  
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
  
    const handleTabKey = (e) => {
      if (e.key !== 'Tab') return;
  
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    };
  
    container.addEventListener('keydown', handleTabKey);
    return () => container.removeEventListener('keydown', handleTabKey);
  }, [isActive]);
  
  return containerRef;
};
```

---

## Development Experience

### Linting and Formatting: Consistency Without Friction

Setting up tools that enforce consistency automatically lets you focus on solving actual problems instead of arguing over code style.

A well-configured ESLint setup catches real issues early—from possible bugs to stylistic mistakes—helping maintain code quality without slowing down development.

### ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'react-app',
    'react-app/jest'
  ],
  rules: {
    // Prevent bugs
    'react-hooks/exhaustive-deps': 'error',
    'no-unused-vars': 'error',
  
    // Code quality
    'prefer-const': 'error',
    'no-var': 'error',
  
    // React best practices
    'react/prop-types': 'warn',
    'react/no-array-index-key': 'warn',
  }
};
```

### Prettier for Code Formatting

Prettier automatically formats code to maintain consistency across the codebase without requiring decisions from developers.

```javascript
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

---

## Conclusion

### The Mindset Shift

The practices we've explored represent more than just technical knowledge. They reflect a **mindset shift toward building software that lasts**.

Every pattern—from state architecture to JSX formatting—serves the same fundamental goal: **Creating code that can grow, adapt, and be understood by the teams that will inherit it.**

### Learning from Experience

These practices didn't come from academic study or theoretical frameworks. They emerged from:
- Countless debugging sessions
- Code reviews
- Refactoring marathons
- Those late-night moments when you finally understood why a particular approach keeps causing problems

### The Journey to Senior Developer

The journey from junior to senior developer isn't about reaching a destination where you've learned everything. It's about developing the **judgment to know when to apply these patterns and, equally important, when to break them**.

Sometimes the "right" architectural decision is the one that gets the feature shipped on time. Sometimes the perfect abstraction is the wrong abstraction for a team that's still learning the domain.

### Staying Relevant

The Frontend landscape will continue to evolve. New frameworks will emerge, old patterns will be questioned, and the "best practices" of today might seem quaint in a few years.

**But the underlying principles remain constant:**
- Clarity
- Maintainability
- Accessibility
- Performance

These are the foundations that allow you to adapt to whatever comes next—whether it's a new state management library, a different bundler, or an entirely new approach to building user interfaces.

### Final Thoughts

Keep building. Keep learning. Remember: **every expert was once a beginner who refused to give up.**

The code you write today will be read and maintained by your future self and your teammates. Make it kind to them. Make it clear. Make it right.

---

## Quick Reference Checklist

- [ ] State is organized into layers (server, global, local, URL)
- [ ] Components have clear boundaries and single responsibilities
- [ ] Custom hooks are extracted for reusable logic
- [ ] Feature-based directory structure is used
- [ ] Exports are optimized for tree shaking
- [ ] JSX is clean and readable with named event handlers
- [ ] Props are well-documented with PropTypes/TypeScript
- [ ] Performance is measured before optimizing
- [ ] Testing follows the pyramid: unit > integration > e2e
- [ ] Code is clearly named and self-documenting
- [ ] Error boundaries and defensive programming are in place
- [ ] Loading and error states are handled as first-class concerns
- [ ] Type safety is implemented with TypeScript or PropTypes
- [ ] Semantic HTML is used throughout
- [ ] Keyboard navigation and focus management are considered
- [ ] ESLint and Prettier enforce consistency
- [ ] Accessibility is built in from the start

---

**Created from:** Senior Frontend Developer Best Practices by Scripting Soul on Medium

Remember: The difference between junior and senior developers isn't just technical skill—it's the intentionality and care put into every decision.
