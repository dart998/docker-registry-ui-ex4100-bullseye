from pathlib import Path

p = Path("/src/src/components/docker-registry-ui.riot")
s = p.read_text(encoding="utf-8")

old = """      <span class=\"logo\">\n        <span><a href=\"{ router.home() }\">{ props.dockerRegistryUiTitle.trim() || \"Docker Registry UI\" }</a></span>"""

new = """      <span class=\"logo\">\n        <a class=\"oscriscloud-brand-image\" href=\"{ router.home() }\" title=\"OsCrisCloud Docker Registry\">\n          <img src=\"oscriscloud-registry-logo.png\" alt=\"OsCrisCloud Docker Registry\" />\n        </a>\n        <span><a href=\"{ router.home() }\">{ props.dockerRegistryUiTitle.trim() || \"Docker Registry UI\" }</a></span>"""

if old not in s:
    raise SystemExit("Expected navbar block not found")
s = s.replace(old, new, 1)

old_css = """    material-navbar .nav-wrapper .logo {\n      display: flex;\n      align-items: center;\n      flex-direction: row;\n    }\n"""

new_css = """    material-navbar .nav-wrapper .logo {\n      display: flex;\n      align-items: center;\n      flex-direction: row;\n      gap: 0.65em;\n    }\n\n    material-navbar .nav-wrapper .logo .oscriscloud-brand-image {\n      display: inline-flex;\n      align-items: center;\n      flex-shrink: 0;\n      text-decoration: none;\n    }\n\n    material-navbar .nav-wrapper .logo .oscriscloud-brand-image:hover {\n      text-decoration: none;\n    }\n\n    material-navbar .nav-wrapper .logo .oscriscloud-brand-image img {\n      display: block;\n      width: 52px;\n      height: 52px;\n      object-fit: cover;\n      border-radius: 10px;\n    }\n"""

if old_css not in s:
    raise SystemExit("Expected navbar CSS block not found")
s = s.replace(old_css, new_css, 1)
p.write_text(s, encoding="utf-8")

index = Path("/src/src/index.html")
html = index.read_text(encoding="utf-8")
needle = '    <meta name="viewport" content="width=device-width, initial-scale=1" />'
replacement = needle + '\n    <link rel="icon" type="image/x-icon" href="favicon.ico" />\n    <link rel="icon" type="image/png" sizes="512x512" href="oscriscloud-registry-favicon.png" />'
if needle not in html:
    raise SystemExit("Favicon insertion point not found")
html = html.replace(needle, replacement, 1)
index.write_text(html, encoding="utf-8")

# Retry transient tag-count errors seen on the EX4100 before displaying a
# false "Server not found" notification.
catalog = Path("/src/src/components/catalog/catalog-element.riot")
cs = catalog.read_text(encoding="utf-8")

old = """      getNbTags(props, state) {\n        const self = this;\n        const oReq = new Http({\n          onAuthentication: props.onAuthentication,\n          withCredentials: props.isRegistrySecured,\n        });\n        oReq.addEventListener('loadend', function () {\n          if (this.status === 200) {\n            const nbTags = (JSON.parse(this.responseText).tags || []).length;\n            self.update({ nbTags });\n          } else if (this.status === 404) {\n            props.onNotify('Server not found', true);\n          } else {\n            props.onNotify(this.responseText, true);\n          }\n        });\n        oReq.addEventListener('error', function () {\n          props.onNotify(this.getErrorMessage(), true);\n        });\n        oReq.open('GET', props.registryUrl + '/v2/' + state.image + '/tags/list');\n        oReq.send();\n      },"""

new = """      getNbTags(props, state, attempt = 0) {\n        const self = this;\n        const maxRetries = 2;\n        const oReq = new Http({\n          onAuthentication: props.onAuthentication,\n          withCredentials: props.isRegistrySecured,\n        });\n        oReq.addEventListener('loadend', function () {\n          if (this.status === 200) {\n            const nbTags = (JSON.parse(this.responseText).tags || []).length;\n            self.update({ nbTags });\n          } else if ((this.status === 0 || this.status === 404 || this.status >= 500) && attempt < maxRetries) {\n            setTimeout(() => self.getNbTags(props, state, attempt + 1), 350 * (attempt + 1));\n          } else if (this.status === 404) {\n            props.onNotify('Server not found', true);\n          } else {\n            props.onNotify(this.responseText || 'Unable to read repository tags', true);\n          }\n        });\n        oReq.addEventListener('error', function () {\n          if (attempt < maxRetries) {\n            setTimeout(() => self.getNbTags(props, state, attempt + 1), 350 * (attempt + 1));\n          } else {\n            props.onNotify(this.getErrorMessage(), true);\n          }\n        });\n        oReq.open('GET', props.registryUrl + '/v2/' + state.image + '/tags/list');\n        oReq.send();\n      },"""

if old not in cs:
    raise SystemExit("Expected getNbTags block not found")
cs = cs.replace(old, new, 1)
catalog.write_text(cs, encoding="utf-8")
