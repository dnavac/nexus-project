/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "surface-bright": "#363a3b",
        "surface-variant": "#323537",
        "tertiary-fixed-dim": "#ffb95f",
        "on-primary-fixed-variant": "#3f465c",
        "surface-dim": "#101415",
        "surface-container-lowest": "#0b0f10",
        "secondary": "#adc6ff",
        "on-primary-fixed": "#131b2e",
        "surface-container": "#1d2022",
        "primary": "#bec6e0",
        "primary-fixed-dim": "#bec6e0",
        "secondary-fixed-dim": "#adc6ff",
        "tertiary-container": "#251400",
        "on-tertiary-fixed": "#2a1700",
        "on-surface-variant": "#c6c6cd",
        "secondary-fixed": "#d8e2ff",
        "on-primary": "#283044",
        "surface-container-highest": "#323537",
        "error-container": "#93000a",
        "inverse-surface": "#e0e3e5",
        "on-background": "#e0e3e5",
        "tertiary-fixed": "#ffddb8",
        "inverse-on-surface": "#2d3133",
        "on-error": "#690005",
        "on-surface": "#e0e3e5",
        "background": "#101415",
        "on-secondary-fixed": "#001a42",
        "on-tertiary": "#472a00",
        "error": "#ffb4ab",
        "surface-container-low": "#191c1e",
        "outline-variant": "#45464d",
        "on-error-container": "#ffdad6",
        "on-primary-container": "#798098",
        "primary-fixed": "#dae2fd",
        "surface-tint": "#bec6e0",
        "on-secondary-fixed-variant": "#004395",
        "on-tertiary-fixed-variant": "#653e00",
        "primary-container": "#0f172a",
        "on-secondary-container": "#e6ecff",
        "on-tertiary-container": "#b47300",
        "secondary-container": "#0566d9",
        "outline": "#909097",
        "inverse-primary": "#565e74",
        "surface": "#101415",
        "on-secondary": "#002e6a",
        "tertiary": "#ffb95f",
        "surface-container-high": "#272a2c"
      },
      borderRadius: {
        DEFAULT: "0.25rem",
        lg: "0.5rem",
        xl: "0.75rem",
        full: "9999px"
      },
      spacing: {
        base: "8px",
        "container-padding-mobile": "20px",
        "element-gap": "16px",
        "container-padding-desktop": "40px",
        gutter: "24px"
      },
      fontFamily: {
        "display-lg-mobile": ["Outfit"],
        "body-md": ["Inter"],
        "display-lg": ["Outfit"],
        "body-lg": ["Inter"],
        "headline-md": ["Outfit"],
        "label-sm": ["Inter"]
      },
      fontSize: {
        "display-lg-mobile": ["32px", { lineHeight: "40px", letterSpacing: "-0.01em", fontWeight: "700" }],
        "body-md": ["16px", { lineHeight: "24px", fontWeight: "400" }],
        "display-lg": ["48px", { lineHeight: "56px", letterSpacing: "-0.02em", fontWeight: "700" }],
        "body-lg": ["18px", { lineHeight: "28px", fontWeight: "400" }],
        "headline-md": ["24px", { lineHeight: "32px", fontWeight: "600" }],
        "label-sm": ["12px", { lineHeight: "16px", letterSpacing: "0.05em", fontWeight: "600" }]
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries')
  ],
}
