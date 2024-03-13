# Security Debt and Vulnerability Propagation in Open Source Software Projects


## Mining and Remediation Time Analysis
In order to verify the pro-activeness of addressing security debt, our study leveraged the National Vulnerability Database (NVD) for comprehensive vulnerability details and employs PyDriller to mine commit data from OSS repositories, aiming to link CVE IDs with specific remediation efforts. The NVD provides a comprehensive database of reported vulnerabilities, including Common Vulnerabilities and Exposures (CVE) identifiers, vulnerability descriptions, severity scores, and dates of disclosure and patching. 

Specifically, we aim to analyze the time taken to address vulnerabilities (remediation time) post their public disclosure and investigate instances of proactive remediation (negative remediation times).

The data was collected using Python scripts that mined GitHub repositories for commits referencing CVE IDs, fetched disclosure dates for these CVEs from the National Vulnerability Database (NVD), and calculated the remediation times for each vulnerability. The analysis focused on two major open-source projects: Django and Rails. Django and Rails were specifically chosen for this analysis due to their significant roles in powering a vast portion of the modern web, serving as exemplary case studies for understanding the security practices and remediation strategies within mature, widely-used open-source web development frameworks


## CodeQL Static Analysis
We utilized multi-variant repository analysis (MRVA) using CodeQL, to identify security vulnerabilities related to well-known issues such as Heartbleed (CVE-2014-0160) stemming from an Apache Struts 2 vulnerability. We leveraged CodeQL’s static analysis engine, wrote custom queries in java and python to model specific vulnerabilities, and analyzed both default repositories provided by MRVA and a custom list of  repositories examined for our case study. Our validation process involved comparing MRVA results with other tools, and we gained insights into exploit behavior which were inconsistent.
