---
title: Confidential Computing
author: Siddarth Senthilkumar
comments: true
date: 2021-09-13 17:44:32
tags:
---

Cloud vendors provide compute power as a utility. This is great for organizations since they can cut costs by taking advantage of economies of scale and offloading datacenter management to a third party. That third party will do a much better job maintaining and securing their machines since that is the core of their business. Most cloud providors even provide SLAs which guarantee certain security and availability requirements are met.

However, for some customers, even the strongest of SLAs is not enough to convince them to move to the cloud. These organizations, typically in government, healthcare, or finance, are legally obligated to take extra precautions when processing data. That's because the data they possess is too sensitive to be accidentally leaked, even just once. A cloud environment faces many threats that they have no control over. What if a malicious actor gains root access to a cloud VM? Or a disgruntled employee at the cloud company decides to install spyware on all the servers? There is very little that the customer can do about these threats since they operate within the typical "trust" boundary - we usually trust that our OS and cloud provider are not intentionally sabotaging us.

Enter confidential computing. With new processor technologies like Intel SGX, application developers can write code that only trusts the processor running their code. These technologies typically encrypt code and data in secure regions of memory called enclaves. Only a genuine processor can decrypt these enclaves and execute the code inside them. Code from outside the enclave cannot modify or even view its contents - even if that code belongs to the OS. This enables sensitive customers to leverage the cloud since they don't even need to trust the cloud provider to run their code properly or safeguard their data.

To prevent an adversary from simply simulating a processor enclave, these technologies come with ways for code within enclaves to attest that they are running on real, secure hardware. An enclave should only continue executing business logic if this attestation succeeds. Typically, this attestation utilizes public key infrastructure (PKI) to cryptographically verify that the sensitive code is running on a genuine platform. Attestation requires public keys embedded in certificates signed by the processor vendor, made available through a web API provided by the vendor.

In Microsoft Azure, the Trusted Hardware Identity Management (THIM) service caches these certificates and other attestation collateral so that Azure can reduce runtime dependencies on third party processor manufacture APIs. Additionally, by serving collateral themselves, Azure can can also schedule security update enforcement at their own pace. In this series of blog posts, I will attempt to explain my understanding of how Intel SGX attestation works and what role the THIM service plays in Azure. Please feel free to leave a comment if you notice anything incorrect! I'm still new in this area and expect a few mistakes here and there.
