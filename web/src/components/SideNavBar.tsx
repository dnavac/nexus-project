export function SideNavBar() {
  return (
    <nav className="hidden lg:flex flex-col fixed left-0 top-0 h-full p-gutter z-40 bg-surface-dim/30 backdrop-blur-2xl w-72 border-r border-white/5 shadow-2xl">
      <div className="flex items-center gap-4 mb-12">
        <div className="h-12 w-12 rounded-full overflow-hidden border border-white/10 bg-surface-container-high flex items-center justify-center">
          <span className="material-symbols-outlined text-secondary font-headline-md">person</span>
        </div>
        <div>
          <h2 className="font-headline-md text-secondary tracking-tight">AI Concierge</h2>
          <p className="font-body-md text-label-sm text-on-surface-variant">Nexus Premium Service</p>
        </div>
      </div>
      <ul className="flex flex-col gap-2 flex-1">
        {/* Active Tab */}
        <li>
          <a className="flex items-center gap-3 p-3 bg-secondary-container/40 text-on-secondary-container rounded-xl font-semibold hover:backdrop-blur-3xl transition-all duration-200" href="#">
            <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>chat_bubble</span>
            New Chat
          </a>
        </li>
        {/* Inactive Tabs */}
        <li>
          <a className="flex items-center gap-3 p-3 text-on-surface-variant hover:bg-white/5 rounded-xl hover:backdrop-blur-3xl transition-all" href="#">
            <span className="material-symbols-outlined">favorite</span>
            Saved Properties
          </a>
        </li>
        <li>
          <a className="flex items-center gap-3 p-3 text-on-surface-variant hover:bg-white/5 rounded-xl hover:backdrop-blur-3xl transition-all" href="#">
            <span className="material-symbols-outlined">analytics</span>
            Investment Analysis
          </a>
        </li>
        <li>
          <a className="flex items-center gap-3 p-3 text-on-surface-variant hover:bg-white/5 rounded-xl hover:backdrop-blur-3xl transition-all" href="#">
            <span className="material-symbols-outlined">person</span>
            Profile
          </a>
        </li>
      </ul>
      <div className="mt-auto flex flex-col gap-4">
        <button className="w-full py-3 rounded-lg bg-secondary-container/20 border border-secondary-container text-secondary font-semibold hover:bg-secondary-container/40 transition-colors">
          Upgrade to Elite
        </button>
        <ul className="flex flex-col gap-2">
          <li>
            <a className="flex items-center gap-3 p-3 text-on-surface-variant hover:bg-white/5 rounded-xl hover:backdrop-blur-3xl transition-all" href="#">
              <span className="material-symbols-outlined">settings</span>
              Settings
            </a>
          </li>
          <li>
            <a className="flex items-center gap-3 p-3 text-on-surface-variant hover:bg-white/5 rounded-xl hover:backdrop-blur-3xl transition-all" href="#">
              <span className="material-symbols-outlined">help</span>
              Support
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
}
