import json

'''
[
    {
        "role": "assistant", 
        "content": "Your mom gay"
    }
]
'''

def condense_ai_msg(msg: str, limit: int = 2000) -> list[str]:
    msg = msg.strip()
    
    if (
        msg.startswith("```") or
        (msg.startswith("{") and msg.endswith("}")) or
        (msg.startswith("[") and msg.endswith("]"))
    ):
        return [msg]
    
    chunks = []
    try: 
        paragraphs = msg.split("\n\n")
        for content in paragraphs: 
            
            while len(content) > limit: 
                window = content[:limit]
                
                # Natural sentence breaks
                split_index = -1
                for delimiter in [". ", "! ", "? "]:
                    split_index = window.rfind(delimiter)
                    if split_index != -1:
                        split_index += len(delimiter)
                        break

                if split_index == -1: 
                    split_index = limit
                
                chunks.append(content[:split_index].strip())
                content = content[split_index:].strip()
            
            if content: 
                chunks.append(content)
                
    except Exception: 
        chunks.append(msg)
        
    return chunks

msg = """
To revise the items you asked for (**\(K_t\), notch sensitivity \(q\), and \(K_f\)**) using the updated strengths \(S_{ut}=120\ \text{ksi}\), \(S_y=66\ \text{ksi}\):

- **\(K_t\)** is **geometric only** → it does **not** change with material strength.
- **\(q\)** (and therefore **\(K_f\)**) **does** depend on material strength through the Peterson/Neuber material constant.

I’ll recompute \(q\) and \(K_f\) using a standard Shigley/Peterson-style approach.

---

## 1) Geometry ratios (same as before)

\[
\frac{D}{d}=\frac{1.510}{1.360}=1.110
\qquad
\frac{r}{d}=\frac{0.076}{1.360}=0.0559
\]

---

## 2) Theoretical stress concentration factor \(K_t\) (bending)

For a round bar with a circumferential groove in **bending**, using charts (Peterson/Shigley) at
\(\,D/d\approx 1.11\), \(r/d\approx 0.056\),

\[
\boxed{K_t \approx 1.6\ \text{(bending)}}
\]

(Still in the ~1.55–1.70 range depending on chart interpolation; I’ll carry 1.6 unless your chart gives a specific value.)

---

## 3) Notch sensitivity \(q\) using Peterson’s relation

Peterson notch sensitivity model:

\[
q=\frac{1}{1+\frac{a}{r}}
\]

where
- \(r = 0.076\ \text{in}\)
- \(a\) is a material constant that depends mainly on \(S_{ut}\)

### Determine \(a\) for steel at \(S_{ut}=120\ \text{ksi}\)
From standard Shigley/Peterson notch-sensitivity data for steels in bending/axial loading, at about \(S_{ut}\approx 120\ \text{ksi}\), a typical value is:

\[
a \approx 0.004\ \text{in}
\]

(That’s the key place the new \(S_{ut}\) matters: stronger steels generally have smaller \(a\), which increases \(q\).)

Now compute \(q\):

\[
q=\frac{1}{1+\frac{0.004}{0.076}}
=\frac{1}{1+0.05263}
=\frac{1}{1.05263}
=0.950
\]

\[
\boxed{q \approx 0.95}
\]

---

## 4) Fatigue stress concentration factor \(K_f\)

\[
K_f = 1 + q\,(K_t - 1)
\]

Substitute \(K_t=1.6\), \(q=0.95\):

\[
K_f = 1 + 0.95(1.6-1)
=1+0.95(0.6)
=1+0.57
=1.57
\]

\[
\boxed{K_f \approx 1.57}
\]

---

# Revised results (with \(S_{ut}=120\ \text{ksi}\), \(S_y=66\ \text{ksi}\))

- \[
\boxed{K_t \approx 1.6}
\]
- \[
\boxed{q \approx 0.95}
\]
- \[
\boxed{K_f \approx 1.57}
\]

---

## Quick check / next step
If you’d like, I can now finish the full problem:
- compute bending stresses at the groove (mean + alternating) from \(M_{\min}=0\) and \(M_{\max}=25{,}000\ \text{lbf·in}\),
- apply \(K_f\) to the alternating component and \(K_t\) to the peak static/yield check,
- compute \(S_e\) with Marin factors (surface = machined at groove; size; bending; etc.),
- then compute:
  - fatigue FOS (Modified Goodman, infinite life)
  - yielding FOS

To do that cleanly, confirm one detail: do you want **yielding** checked using **nominal stress with \(K_t\)** (common) or using a **local plasticity approach** (less common in this type of homework)?
"""

results = condense_ai_msg(msg)
with open("test.json", "w") as j: 
    json.dump(results, j, indent=4)
    
