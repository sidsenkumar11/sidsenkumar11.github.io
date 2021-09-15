---
title: Intel SGX Attestation Part 1
author: Siddarth Senthilkumar
comments: true
date: 2021-09-13 21:21:04
tags:
---

## What is Remote Attestation?

Intel SGX is a set of processor extensions for establishing enclaves. Enclaves are trusted execution environments whose code and data cannot be accessed outside the enclave - even by the application that created it or by the operating system. An attacker that wishes to inspect the contents of an enclave may try to emulate the hardware. The process of proving that the enclave has been established in a secure hardware environment is known as attestation. In the cloud, remote attestation gives enclave authors the ability to remotely verify that their code is running on genuine, secure SGX hardware.

Note: the term "enclave" is used to denote both a signed binary file as well as the encrypted memory where the binary is loaded at runtime. To disambiguate, I will refer to the binary as the enclave binary and to the encrypted memory as the enclave.

## Secure Enclave Instantiation

It would be meaningless for an enclave to perform attestation if the code in the enclave could be modified by an attacker. So before we can understand how remote attestation works, we must first understand how the processor securely loads enclave binaries into memory.

To do this, we introduce two properties of an enclave: the MRENCLAVE and MRSIGNER. These are two registers introduced by the SGX architecture and are set by the hardware when an enclave is instantiated.

- **MRENCLAVE** - Represents the enclave identity. Contains the SHA256 hash of an internal log that records all the activity during enclave instantiation. This includes the contents of the enclave memory pages (code/data/stack/heap), the order and relative position in which the enclave's pages were placed, and any security flags associated with the pages. The MRENCLAVE value is also known as the enclave _measurement_.

- **MRSIGNER** - Represents the sealing identity. An enclave author must sign their enclave binary with an RSA private key. The MRSIGNER is a hash of the corresponding public key certificate (typically self-signed).

### Why are these registers important?

The MRENCLAVE is like a hash of all the memory pages, data, and security flags of the freshly loaded enclave memory. If this value can somehow be verified, then the enclave can at least be sure its code and data were not tampered.

The MRSIGNER provides a way to authenticate the enclave. If multiple enclaves are signed by the same enclave author, they will have the same MRSIGNER. The Sealing Identity can be used to seal data in a way that enclaves from the same Sealing Authority can share and migrate their sealed data.

### How are these registers set?

A part of the enclave binary is a structure called the MRSIGN struct. It contains the expected MRENCLAVE value, the RSA public key of the enclave author, and a signature over the whole enclave binary.

Before an enclave is instantiated, the author's identity is first verified using the public key. If the public key verifies the signature over the enclave, we know that the self-signed certificate containing the public key really does represent the enclave author.

Then, the MRENCLAVE value from the struct is copied to the MRENCLAVE register. The CPU begins loading pages into memory and setting security flags on those pages. As it does this, it keeps a log of what data is being loaded and set. At the end, this log is hashed and compared with the MRENCLAVE in the register. If they match, then the CPU knows that the enclave binary was not tampered with and can safely begin executing enclave code.

Finally, the MRSIGNER is stored in the MRSIGNER register. It is simply a hash of the enclave author's public key. Now, both the MRENCLAVE and MRSIGNER are available for use within the enclave for sealing data and attestation. Naturally, only the CPU can write to these registers - they cannot be overwritten after enclave instantiation.

## References

- https://software.intel.com/content/www/us/en/develop/articles/innovative-technology-for-cpu-based-attestation-and-sealing.html

- https://community.intel.com/t5/Intel-Software-Guard-Extensions/Question-about-MRENCLAVE-and-MRSIGNER-Register-used-in/m-p/1070695/highlight/true

- https://software.intel.com/content/www/us/en/develop/download/intel-sgx-intel-epid-provisioning-and-attestation-services.html
