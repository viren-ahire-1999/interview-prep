from util import topic, diagram, callout, code


def k8s() -> str:
    t1 = topic("k8s-objects", "The objects you will actually touch",
               "kubernetes pod namespace service route CRD oc", "Lesson",
               """
  <p>You do not need to pass a CKA. You need to <b>read a cluster the way a plugin author debugs</b>: “is my UI even installed, and can this user reach Loki?”</p>
  <p>A <b>cluster</b> is the whole computer. A <b>namespace</b> is a named folder inside it (shop, openshift-monitoring, your plugin’s namespace). Most Observe objects you care about are namespaced. Cluster-scoped things (Console, some operators) are global.</p>
  <table>
    <tr><th>Object</th><th>Plain English</th><th>Why Observe UI cares</th></tr>
    <tr><td>Pod</td><td>One running process group</td><td>Logs attach to a container in a pod. CrashLoop is a pod status.</td></tr>
    <tr><td>Deployment / StatefulSet</td><td>Keep N pods alive</td><td>Restart counts, desired vs ready — metrics and the workload page.</td></tr>
    <tr><td>Service</td><td>Stable in-cluster DNS + port</td><td>ConsolePlugin <code>spec.proxy</code> points at a Service, not a Pod IP.</td></tr>
    <tr><td>Route / Ingress</td><td>How humans hit HTTP from outside</td><td>The console itself is a Route. Plugin assets are usually <i>not</i> a public Route; the console proxies them.</td></tr>
    <tr><td>ConfigMap / Secret</td><td>Config vs sensitive config</td><td>Feature flags, Loki tenant, TLS CA. Do not log Secrets.</td></tr>
    <tr><td>Custom Resource (CR)</td><td>A typed YAML object an operator watches</td><td><code>ConsolePlugin</code>, <code>UIPlugin</code>, Perses dashboards — this is how UI is installed.</td></tr>
    <tr><td>CRD</td><td>The schema for that CR</td><td>If the CRD is missing, <code>oc apply</code> of the CR fails. Not a Webpack bug.</td></tr>
  </table>
  """ + diagram("""You apply YAML  →  API server stores the object
Operator / controller watches  →  creates Deployments, Services, …
Pods run  →  your plugin JS is served from a Service
Console reads ConsolePlugin list  →  browser loads the remote entry""") + """
  <p><b>oc vs kubectl.</b> On OpenShift, <code>oc</code> is kubectl plus login, projects (namespaces), and Routes. Commands you will type daily:</p>
  """ + code("Bash", '''oc login --server=...          # or use a kubeconfig
oc project openshift-console   # set namespace
oc get consoleplugins
oc get uiplugins
oc get pods -n my-plugin
oc logs -n my-plugin deploy/my-plugin
oc describe consoleplugin example-observe
oc get console cluster -o yaml   # spec.plugins lives here''') + """
  """ + callout("If the UI is missing, read the cluster before Chrome DevTools. Order: Console <code>spec.plugins</code> → UIPlugin / operator → plugin Pod → then the browser."), "topics")

    t2 = topic("k8s-rbac", "RBAC is why the same query is empty for one user",
               "RBAC Role RoleBinding ServiceAccount user token", "Lesson",
               """
  <p>Kubernetes authorization is not “hide the button.” The API returns 403. Observe UIs that call Loki, Prometheus, or Tempo <b>as the logged-in user</b> (UserToken on the proxy) will show empty or error depending on that user’s RoleBindings.</p>
  <ul>
    <li>A <b>Subject</b> is a user, group, or ServiceAccount.</li>
    <li>A <b>Role</b> (namespace) or <b>ClusterRole</b> (cluster) lists verbs + resources (<code>get/list/watch</code> on pods, or a custom resource).</li>
    <li>A <b>RoleBinding</b> attaches the Role to the Subject in one namespace.</li>
  </ul>
  """ + code("YAML", '''apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: read-pods
  namespace: shop
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devs-read-pods
  namespace: shop
subjects:
  - kind: Group
    name: shop-devs
roleRef:
  kind: Role
  name: read-pods
  apiGroup: rbac.authorization.k8s.io''') + """
  <p><b>UI implication.</b> Empty logs can mean “no lines” or “this user cannot list that namespace.” Those are different empty states. Copy must not say “no errors found” when the API said 403.</p>
  <p>Loki often has a <b>tenant</b> (OrgID) as well as Kubernetes RBAC. Tempo has retention. Prometheus may have namespace-scoped access via kube-rbac-proxy. You translate those backend contracts into UI, you do not bypass them in the frontend.</p>
  """ + callout("Never send a cluster-admin token from the plugin ‘to make the demo work.’ UserToken exists so the graph shows what <i>this</i> user is allowed to see."), "topics")

    t3 = topic("k8s-gitops", "GitOps can undo a UI click",
               "GitOps Console spec.plugins ArgoCD", "Lesson",
               """
  <p>Many clusters reconcile the <b>Console</b> custom resource from git. The console Operator enables dynamic plugins listed in <code>spec.plugins</code>. If you toggle a plugin in the UI (or apply a CR by hand) and git does not contain that name, the next sync <b>removes it</b>.</p>
  """ + code("YAML", '''apiVersion: operator.openshift.io/v1
kind: Console
metadata:
  name: cluster
spec:
  plugins:
    - monitoring
    - logging-view-plugin
    - troubleshooting-panel''') + """
  <p>This is the #1 “my plugin vanished overnight” story. It looks like a frontend regression. It is an operations contract. Your architecture one-pager should mention it.</p>
  """ + diagram("""Git  --reconcile-->  Console.spec.plugins
                         |
                         v
              console Operator enables those names only
A live UI toggle not in git  →  next sync deletes it"""), "topics")
    return f'''
<section class="block" id="k8s" data-search="Kubernetes primer oc RBAC CRD" data-stype="Section">
  <p class="kicker">Cluster literacy</p>
  <h2 class="section-title">Kubernetes enough</h2>
  <p class="lede">This is not a Kubernetes course. It is the slice you need so plugin YAML, empty states, and “the UI disappeared” are not mysteries. Mark complete when you can read a ConsolePlugin and a RoleBinding without a cheatsheet.</p>
  {t1}{t2}{t3}
</section>
'''
