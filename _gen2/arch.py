from util import code, topic, diagram, callout


def fundamentals() -> str:
    t1 = topic("fund-boundaries", "Boundaries, coupling, cohesion, contracts", "frontend architecture coupling cohesion", "Architecture", f'''
  <p><b>Mental model.</b> A frontend architecture is a set of <i>allowed dependencies</i>. If any file can import any other file, you do not have an architecture — you have a pile. Seniors design the arrows, not the folder names.</p>
  <p><b>Coupling</b> is how much A must change when B changes. <b>Cohesion</b> is how much the pieces inside a module serve one reason to change. You want high cohesion, low coupling, and <b>dependency direction</b> that points inward toward stable policy (UI → application use-cases → domain types → infrastructure adapters).</p>
  <p><b>A boundary</b> is a line where a contract exists: a TypeScript public export, an event, an HTTP API, a design-system package. Crossing a boundary without the contract is a bug, even if TypeScript compiles.</p>
  {diagram('''UI components  -->  feature hooks / use-cases
        |                    |
        v                    v
   design system         domain types + ports
                             |
                             v
                    adapters (HTTP, analytics, flags)''')}
  <p><b>Extensibility</b> is cheap when new features add modules that implement a port. <b>Maintainability</b> dies when every feature reaches into every other feature’s Redux slice or CSS global.</p>
  <p><b>Interview.</b> “How do you keep 20 engineers from creating a dependency mess?” Answer: package boundaries + lint (dependency-cruiser / eslint-plugin-import) + a small number of public barrels + code review that rejects cross-feature deep imports. Not “we use monorepo.”</p>
  {callout("Atlassian-shaped products last a decade. The architecture that ships the next plugin without rewriting issue-view is the architecture that wins.", "good")}
''', "topics")

    t2 = topic("fund-shapes", "Monolith, modular monolith, feature and layered shapes", "modular monolith feature-based layered clean architecture", "Architecture", f'''
  <p>None of these is universally correct. Pick from constraints: team count, deploy independence, shared domain, plugin surface.</p>
  <table>
    <tr><th>Shape</th><th>What it is</th><th>When it works</th><th>When it fails</th></tr>
    <tr><td>SPA monolith</td><td>One build, one repo, shared runtime</td><td>&lt; ~3 teams, one product</td><td>Release trains block everyone; compile times explode</td></tr>
    <tr><td>Modular monolith</td><td>One deploy, hard module boundaries</td><td>Most Atlassian-like products</td><td>If boundaries are only folders, they rot</td></tr>
    <tr><td>Feature-based</td><td>Vertical slices: issues/, board/, search/</td><td>Teams own a user journey</td><td>Shared “god” utils/ and store/</td></tr>
    <tr><td>Layered</td><td>components / hooks / services / api</td><td>Small apps, shared tech</td><td>Every change touches 5 layers; features leak everywhere</td></tr>
    <tr><td>DDD-lite frontend</td><td>features + entities + shared kernel</td><td>Rich domain (issue, sprint, space)</td><td>Over-modeling CRUD screens</td></tr>
    <tr><td>Micro-frontends</td><td>Independent deploy + integrate</td><td>True org/deploy isolation</td><td>Shared UX, shared issue object, tight coupling</td></tr>
  </table>
  <h4>Feature-sliced example (good default for 20 engineers)</h4>
  {code("text", '''src/
  app/                 # shell: router, providers, boot
  pages/               # route-level composition only
  features/
    issue-view/
    board/
    search/
    admin/
  entities/
    issue/             # types, mappers, tiny UI atoms used by many features
    user/
  shared/
    ui/                # design-system wrappers if not a package
    lib/               # date, i18n — no feature imports
    api/               # HTTP client, error mapping
    analytics/
    flags/
    auth/''')}
  <p><b>Why this works:</b> a board engineer lives in <code>features/board</code>. They may import <code>entities/issue</code> and <code>shared/*</code>. They may not import <code>features/admin</code>. Dependency-cruiser enforces it in CI.</p>
  <p><b>When it does not:</b> if “entities/issue” becomes a dumping ground for board-specific cells, or if features communicate by writing each other’s Redux keys. Then you have a distributed monolith in one folder tree.</p>
  <h4>Layered alternative (fine under ~8 people)</h4>
  {code("text", '''src/
  components/  hooks/  services/  store/  utils/  pages/''')}
  <p>This is easier to start and harder to own. Every new screen adds files in five places. Prefer it for a greenfield spike; migrate to features when the second team arrives.</p>
  <p><b>Clean/hexagonal idea (keep it light):</b> features depend on ports (<code>IssueRepository</code>). Adapters implement fetch. Tests fake the port. Do not invent 12 layers for a settings form.</p>
  {callout("Trade-off sentence to practice: “I’d start with a modular monolith, feature folders, and enforced import rules. I would not split deployables until a team is blocked on release cadence or a runtime isolation requirement (plugins, different SLO).\"")}
''', "topics")

    return f'''
<section class="block" id="fundamentals" data-search="Frontend Architecture Fundamentals" data-stype="Section" data-cat="architecture">
  <p class="kicker">Foundations</p>
  <h2 class="section-title">Frontend Architecture Fundamentals</h2>
  <p class="lede">Senior interviews are won by talking about arrows, ownership, and failure modes — not by reciting “we use React.”</p>
  {t1}{t2}
</section>
'''


def react_arch() -> str:
    t = topic("ra-prod", "Architecting a production React application", "React architecture error boundaries feature flags services", "React architecture", f'''
  <p>A production React app is a <b>composition root</b> plus feature modules. The shell owns routing, providers (auth, flags, query client, theme), and error boundaries. Features own screens and their hooks. Shared infrastructure is imported, never copy-pasted.</p>
  {diagram('''app/boot
  QueryClient + Auth + Flags + Theme + Router
       |
       +-- ErrorBoundary (route)
       +-- pages/IssuePage  --> features/issue-view
       +-- pages/BoardPage  --> features/board
                 |
                 +-- widgets (presentational)
                 +-- useIssue(id)  --> api/issues (port)
                 +-- analytics.track
                 +-- flags.isOn('issue-ai')''')}
  <ul class="tight">
    <li><b>Component boundaries:</b> a component that both fetches and paints a 400-line JSX file is not a boundary. Split “data + policy” (hook) from “view” (props in, events out).</li>
    <li><b>Smart vs presentational:</b> still useful if you treat “smart” as a hook, not a class container. Presentational components are the design-system and widgets; they are easy to Storybook and a11y-test.</li>
    <li><b>Service / API client:</b> one HTTP client (timeouts, correlation ID, 401 refresh, error mapping). Features call <code>issuesApi.get(id)</code>, not <code>fetch</code> inline.</li>
    <li><b>Context boundaries:</b> split providers by change rate (theme vs current-user vs live-board). One mega-context is a re-render bomb.</li>
    <li><b>Error boundaries:</b> at route and at expensive widgets (board, editor). A plugin crash must not white-screen Jira. Pair with an error-reporting client and a fallback UI.</li>
    <li><b>Routing:</b> URL is a public API. Filters, selected issue, and tab belong in the URL if they are shareable. Nested routes for issue-in-board.</li>
    <li><b>Feature flags:</b> evaluated at the edge of a feature, not sprinkled as <code>if (flag)</code> in 40 files. Server-driven flags; never assume the client is the source of truth for entitlements.</li>
    <li><b>Config / env:</b> build-time public env vs runtime config endpoint (different CDN builds per realm). Do not bake tenant URLs you cannot change.</li>
    <li><b>Permissions:</b> hide and disable in UI, <i>enforce on the server</i>. Frontend permission hooks are UX, not security.</li>
    <li><b>Analytics / logging:</b> a telemetry port. Features emit intent (“issue_transitioned”), the adapter maps to the vendor. PII policy lives in the adapter.</li>
  </ul>
  {code("TypeScript", '''// Feature hook: policy + data. The view does not know TanStack Query.
export function useIssue(id: string) {
  const q = useQuery({ queryKey: ["issue", id], queryFn: () => issuesApi.get(id) });
  const canEdit = usePermission("issue", id, "edit");
  return { issue: q.data, status: q.status, canEdit, reload: q.refetch };
}''')}
  <p><b>Complete large-app picture (Jira-like):</b> app shell; features for board, issue-view, search, admin; entities for Issue/User/Project; shared query client; design-system package; plugin sandbox iframe; flags + analytics adapters; route-level and widget-level error boundaries; observability (RUM + traces) initialized in boot.</p>
''', "topics")
    t2 = topic("ra-comp", "Component design and composition", "component API composition headless", "Architecture", f'''
  <p>A component API is a contract. Prefer composition (<code>Modal.Header</code>) over boolean soup (<code>isLarge isDanger showFooter hideClose</code>). Headless primitives (focus trap, listbox) + styled skins scale across brands.</p>
  <p><b>Common mistake:</b> exporting a 60-prop <code>Table</code> that every product forks. Better: headless row model + slots + a few product tables that compose it.</p>
  {callout("Interview takeaway: show you can say no to a prop and propose a slot instead.")}
''', "topics")
    return f'''
<section class="block" id="react-arch" data-search="React Architecture production application" data-stype="Section" data-cat="architecture">
  <p class="kicker">Production React</p>
  <h2 class="section-title">React Architecture</h2>
  <p class="lede">Beyond “components and hooks”: the shell, the ports, and the lines features may not cross.</p>
  {t}{t2}
</section>
<section class="block" id="components" data-search="Component Design APIs composition" data-stype="Section" data-cat="architecture">
  <p class="kicker">APIs</p>
  <h2 class="section-title">Component Design</h2>
  <p class="lede">A component is a public API. Seniors design the contract first: what is owned, what is composed, what is forbidden.</p>
  {topic("comp-api", "Component contracts, composition, and ownership", "component API composition slots headless presentational", "Component design", f'''
  <p><b>Mental model.</b> Every exported component has callers you do not control. Props are a versioned interface. A boolean that exists only for one product screen is a smell; a slot or a smaller primitive is usually the fix.</p>
  <h4>Three layers (use all three, do not collapse them)</h4>
  <ol>
    <li><b>Headless primitive</b> — focus, keyboard, roles, open/close state. No pixels. Example: a listbox that speaks the APG pattern.</li>
    <li><b>Styled primitive</b> — tokens, density, icons. Example: <code>Menu</code> that looks like your DS.</li>
    <li><b>Product pattern</b> — domain meaning. Example: <code>IssueStatusLozenge</code> knows statuses, not a generic <code>Badge variant="purple"</code> used 40 ways.</li>
  </ol>
  {diagram('''IssuePage
  -> IssueHeader (product pattern)
       -> Heading + Lozenge + AvatarStack  (DS composites)
            -> Text, Pressable, FocusRing   (primitives)
  IssuePage owns data + permissions.
  IssueHeader owns layout of that slice.
  Lozenge owns color + a11y name, not Jira workflow rules.''')}
  <h4>Smart vs presentational — the 2026 version</h4>
  <p>Do not recreate 2016 “container components” as classes. <b>Smart</b> is a hook or a thin route module: <code>useIssue(id)</code> returns data + permissions + actions. <b>Presentational</b> receives props and fires events. The presentational layer is what you Storybook, screenshot, and a11y-test without MSW.</p>
  <p>A 400-line component that fetches, branches on flags, and paints the page is not “pragmatic.” It is an untestable ownership blob. Split when a file has two reasons to change (data policy vs visual layout).</p>
  <h4>API design rules that survive 20 engineers</h4>
  <table>
    <tr><th>Prefer</th><th>Avoid</th><th>Why</th></tr>
    <tr><td>Composition: <code>Modal.Header</code>, children, slots</td><td><code>showFooter hideClose isDanger isLarge</code></td><td>Boolean soup cannot express the next variant</td></tr>
    <tr><td>Explicit events: <code>onTransition(id)</code></td><td>Reaching into a ref to call <code>submit()</code></td><td>Callers need a data flow they can test</td></tr>
    <tr><td>Polymorphic <code>as</code> or <code>render</code> when you must</td><td>Copy-pasting Button for LinkButton for MenuButton</td><td>One focus/disabled story</td></tr>
    <tr><td>Controlled + uncontrolled with a documented default</td><td>Half-controlled inputs</td><td>The classic “value + defaultValue” bug</td></tr>
    <tr><td>Types that make illegal states unrepresentable</td><td><code>error?: string; loading?: boolean; data?: T</code> all optional</td><td>Use a discriminated union for status</td></tr>
  </table>
  {code("TypeScript", '''type IssueCardProps = {
  issue: IssueSummary;
  selected?: boolean;
  onOpen: (id: string) => void;
  trailing?: React.ReactNode; // slot, not showAssignee showPriority showEpic
};
// Illegal state made hard:
type QueryView<T> =
  | { status: "loading" }
  | { status: "error"; error: Error; retry: () => void }
  | { status: "success"; data: T };''')}
  <h4>State that belongs in the component vs the page</h4>
  <ul class="tight">
    <li>Hover, open/close of a local menu, ephemeral highlight → local.</li>
    <li>Selected issue, filter, tab that is shareable → URL / page.</li>
    <li>Fetched issue body → server cache, not <code>useState</code> in the card.</li>
  </ul>
  <p><b>When this structure fails:</b> over-abstracting a one-off admin screen into a “generic engine”; under-abstracting a table that 8 teams will copy. The interview answer is the rule plus an example of when you would break it.</p>
  {callout("Practice question: “Design a reusable Modal.” Lead with focus restore, Escape, backdrop, portal, labelled-by, and a slot API. Do not start with CSS.")}
  ''', "topics")}
</section>
<section class="block" id="scale" data-search="Frontend Scalability multi-team" data-stype="Section" data-cat="architecture">
  <p class="kicker">Many teams</p>
  <h2 class="section-title">Frontend Scalability</h2>
  <p class="lede">Scale here means <b>people and time</b>, not only QPS. A 200ms INP and a 20-minute CI are both scalability bugs.</p>
  {topic("scale-people", "Scaling the codebase with teams", "frontend scalability monorepo ownership", "Architecture", f'''
  <ul class="tight">
    <li><b>Ownership:</b> CODEOWNERS per feature package. Review load is a first-class SLO.</li>
    <li><b>Build:</b> incremental tsc / project references, affected-test (Nx/Turborepo). A 5-minute main build that is 40 minutes on a Friday afternoon is an architecture problem.</li>
    <li><b>Shared kernel:</b> keep it small. The more that lives in shared/, the more you recreate a monolith with extra steps.</li>
    <li><b>Compatibility:</b> design-system and entity types version like public APIs. Deprecate, don’t break on a Tuesday.</li>
    <li><b>Runtime scale:</b> code-split by route and by heavy widgets (editor, board). Do not download admin settings JS on the issue view.</li>
  </ul>
  <p>Practice question: “How would you structure a React monorepo used by 20 teams?” — packages by domain, one app shell, enforced deps, shared DS, CI affected graph, RFC process for kernel changes.</p>
  ''', "topics")}
</section>
'''
