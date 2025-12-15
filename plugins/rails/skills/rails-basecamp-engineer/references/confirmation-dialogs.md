# Confirmation Dialogs

Native HTML `<dialog>` confirmations with Turbo integration for destructive actions.

## Overview

Modern browsers support styled confirmation dialogs without custom JavaScript through:
- `command`/`commandfor` attributes for declarative dialog control
- `@starting-style` CSS rules for enter animations
- `closedby` attribute for backdrop dismissal
- Native accessibility with ARIA support

## Basic Dialog Pattern

### HTML Structure

```erb
<button type="button" commandfor="delete-item-dialog" command="show-modal">
  Delete this item
</button>

<dialog id="delete-item-dialog" closedby="any" role="alertdialog"
        aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <header>
    <hgroup>
      <h3 id="dialog-title">Delete this item?</h3>
      <p id="dialog-desc">Are you sure you want to permanently delete this item?</p>
    </hgroup>
  </header>

  <footer>
    <button type="button" commandfor="delete-item-dialog" command="close">
      Cancel
    </button>
    <%= button_to item_path(item), method: :delete do %>
      Delete item
    <% end %>
  </footer>
</dialog>
```

### Key Attributes

| Attribute | Purpose |
|-----------|---------|
| `commandfor` | Target dialog by ID |
| `command="show-modal"` | Open as modal dialog |
| `command="close"` | Close the dialog |
| `closedby="any"` | Enable backdrop click dismissal |
| `role="alertdialog"` | Signal importance for accessibility |

## CSS Animations

### Enter and Exit Animations

```css
dialog {
  opacity: 1;
  scale: 1;
  transition:
    opacity 0.2s ease-out,
    scale 0.2s ease-out,
    overlay 0.2s ease-out allow-discrete,
    display 0.2s ease-out allow-discrete;

  @starting-style {
    opacity: 0;
    scale: 0.95;
  }
}

dialog:not([open]) {
  opacity: 0;
  scale: 0.95;
}
```

### Backdrop Styling

```css
dialog::backdrop {
  background-color: rgb(0 0 0 / 0.5);
  transition:
    background-color 0.2s ease-out,
    overlay 0.2s ease-out allow-discrete,
    display 0.2s ease-out allow-discrete;

  @starting-style {
    background-color: rgb(0 0 0 / 0);
  }
}
```

### Prevent Background Scroll

```css
body:has(dialog:modal) {
  overflow: hidden;
}
```

## Turbo Integration

### Global Dialog Template

Add to your layout for Turbo-powered confirmations:

```erb
<%# app/views/layouts/application.html.erb %>
<dialog id="turbo-confirm-dialog" closedby="any"
        aria-labelledby="turbo-confirm-title" aria-describedby="turbo-confirm-message">
  <header>
    <hgroup>
      <h3 id="turbo-confirm-title">Confirm</h3>
      <p id="turbo-confirm-message"></p>
    </hgroup>
  </header>

  <footer>
    <button type="button" commandfor="turbo-confirm-dialog" command="close">
      Cancel
    </button>
    <form method="dialog">
      <button type="submit" value="confirm">
        Confirm
      </button>
    </form>
  </footer>
</dialog>
```

### JavaScript Configuration

Configure Turbo's confirmation handler:

```javascript
// app/javascript/application.js
const dialog = document.getElementById("turbo-confirm-dialog")
const messageElement = document.getElementById("turbo-confirm-message")
const confirmButton = dialog?.querySelector("button[value='confirm']")

Turbo.config.forms.confirm = (message, element, submitter) => {
  if (!dialog) return Promise.resolve(confirm(message))

  messageElement.textContent = message

  const buttonText = submitter?.dataset.turboConfirmButton || "Confirm"
  confirmButton.textContent = buttonText

  dialog.showModal()

  return new Promise((resolve) => {
    dialog.addEventListener("close", () => {
      resolve(dialog.returnValue === "confirm")
    }, { once: true })
  })
}
```

## Rails Usage Examples

### Basic Confirmation

```erb
<%= button_to item_path(@item),
              method: :delete,
              data: { turbo_confirm: "Are you sure you want to delete this item?" } do %>
  Delete
<% end %>
```

### Custom Button Text

```erb
<%= button_to item_path(@item),
              method: :delete,
              data: {
                turbo_confirm: "Are you sure you want to delete this item?",
                turbo_confirm_button: "Delete item"
              } do %>
  Delete
<% end %>
```

### Link with Confirmation

```erb
<%= link_to "Archive",
            archive_project_path(@project),
            data: {
              turbo_method: :patch,
              turbo_confirm: "Archive this project?",
              turbo_confirm_button: "Archive"
            } %>
```

## Accessibility

The implementation provides:

- `role="alertdialog"` to communicate importance to assistive technology
- `aria-labelledby` connecting the title heading
- `aria-describedby` connecting the description text
- Automatic Escape key handling via native dialog
- Screen reader announcement of full context
- Focus trapping within modal

## Browser Support

| Feature | Chrome | Safari | Firefox |
|---------|--------|--------|---------|
| `command` | 135+ | 26.2+ | 144+ |
| `commandfor` | 135+ | 26.2+ | 144+ |
| `@starting-style` | 117+ | 17.5+ | 129+ |
| `closedby` | 134+ | Pending | 141+ |

### Polyfills

For older browser support, include these polyfills:

- `dialog-closedby-polyfill` - Adds `closedby` attribute support
- `invokers-polyfill` - Adds `command`/`commandfor` support

The JavaScript configuration falls back to native `confirm()` when the dialog element is not found, providing graceful degradation.
