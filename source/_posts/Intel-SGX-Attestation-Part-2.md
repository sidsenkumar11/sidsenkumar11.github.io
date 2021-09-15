---
title: Intel SGX Attestation Part 2
author: Siddarth Senthilkumar
comments: true
date: 2021-09-14 20:47:24
tags:
---

## Local Attestation

After an SGX enclave has been instantiated on a platform, it may want to attest or prove that it is running on genuine SGX hardware. Before we talk about how it can prove this to remote parties, we will first discuss local attestation. Local attestation is when an enclave proves to another enclave on the same host that they are running on the same, genuine SGX hardware.

### Motivation

You may be wondering why an enclave would care to attest itself to another enclave. Imagine the following scenario: Netflix is streaming videos to your computer. Netflix doesn't want you to save their videos since they are copyright protected. But, they have to send you the video somehow so you can play it. How can they accomplish this?

If they send the video encrypted in an enclave binary, then you would not be able to view the raw video binary - only the CPU would be able to decode and play the video. But the enclave needs to first know if if it's running on a genuine SGX platform. So, the enclave will want to attest itself with another enclave on your computer - maybe one written and signed by Intel for the sole purpose of verifying other enclaves. For this, we need a local attestation mechanism.

### Procedure

Intel SGX introduced a new instruction called "EREPORT". When invoked by an enclave, EREPORT asks the hardware to produce a signed structure called a report. The key used to sign is called the report key. The report key can only be requested from the hardware by the verifying enclave, so only the verifying enclave can properly verify the signature of this report. In other words, each enclave has a unique report key that only it can access, but other enclaves can still ask for reports signed by it.

The report contains the MRSIGNER, MRENCLAVE, some attributes associated with the enclave, and the hardware TCB\*. The report also contains a small user-data field so the enclave author can include some miscellaneous data in the report. The user data must be passed to the EREPORT instruction as an argument.

Then, the source enclave takes this report and sends it to the verifying enclave. The verifying enclave first checks the signature on the report. To do this, it gets its report key via the EGETKEY instruction. If the report was signed properly, then the verifying enclave knows both enclaves are running on the same platform. Finally, the verifying enclave generates its own report and sends that report to the original enclave so the original enclave can verify it.

\* Don't worry about the meaning of hardware TCB for now. Just know it has something to do with the "security level" of the hardware.

### Establishing a Secure Channel between Enclaves

Let's say the two enclaves wish to establish a secure channel with each other. This means they want to send each other encrypted messages, since they can't trust the application hosting them to send the data unadultered. Establishing a secure channel requires them to exchange session keys which can be used to encrypt their messages.

They can do this using the report's user data section. The user data section is only 256 bits long, so typically an application enclave will just hash the real data they want to pass and provide the hash in the report. Then, the application enclave will send both the report and the session key to the target enclave. The target enclave can verify that the hash of the attached user data matches the hash in the user data section of the report.

## Summary

To summarize, local attestation is performed through the following steps:

1. Enclave A obtains enclave B's MRENCLAVE value through some insecure path.
2. Enclave A generates some data which can be used to provision a secure channel (e.g. diffie hellman key).
3. Enclave A invokes EREPORT with two arguments: enclave B's MRENCLAVE and a hash of the user data from the previous step. This tells the hardware to create a report and sign it using Enclave B's report key. The hash of the user data should be in the user data field of the report.
4. Enclave A sends the signed report and user data to enclave B. This can happen over an untrusted channel.
5. Enclave B receives the report. First, it uses EGETKEY to retrieve its report key and recompute the MAC over the report. If it matches, then A really is an enclave running on the same platform as B, in an environment that abides by Intel SGX's security model.
6. Enclave B verifies that the user data was properly received by checking the hash in the report against the hash of the user data received.
7. Enclave B creates a report for A by using the MRENCLAVE from the report it just received. It may attach its own user data for key exchange.
8. Enclave B transmits its report to A, and A verifies the report + user data.
9. Now, both enclaves can use their new session key generated from the user data to exchange encrypted information.

## References

- https://www.blackhat.com/docs/us-17/thursday/us-17-Swami-SGX-Remote-Attestation-Is-Not-Sufficient-wp.pdf

- https://software.intel.com/content/www/us/en/develop/articles/innovative-technology-for-cpu-based-attestation-and-sealing.html
