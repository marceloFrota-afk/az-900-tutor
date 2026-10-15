The first 30-item review is preserved below. See the [65-item continuation and independent AI review](questions-review-2026-10-15.md) and [human review packet](human-review-pack.md) for current scope and remaining work.

# Independent question review

Date: **2026-10-15**. Reviewer: a second AI agent, separate from the question author. All 30 prompts, keys, rubrics, distractors and primary competency mappings were read. Seven questions are multiple choice (Q002, Q005, Q007, Q012, Q016, Q022, Q029); their current keys are respectively **B, A, C, B, C, B, A**. No key change was required, but two questions needed greater precision.

## Corrections

- **Q016:** Generic mountable file-protocol support was insufficient to cleanly distinguish Azure Files from Blob Storage, which can expose NFS 3.0. The prompt now specifically requires **SMB** and the Blob distractor explanation acknowledges NFS. Evidence: [Azure Files](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-introduction), [Blob NFS support](https://learn.microsoft.com/en-us/azure/storage/blobs/network-file-system-protocol-support).
- **Q021:** “Read resources” could mean resource configuration or their stored data. The prompt now asks for configuration visibility; its answer specifies that the built-in Reader role has control-plane read actions and no DataActions. Evidence: [Reader role](https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/general#reader).
- **Q030:** Corrected a Portuguese verb form. The conceptual distinction between platform incident reporting and application telemetry was retained.
- **Assessment documentation:** Corrected the multiple-choice count from nine to seven. Updated review status to distinguish this AI editorial review from a human Azure specialist review and empirical item validation.

## Source families checked

| Items | Distinction reviewed | Official evidence |
| --- | --- | --- |
| Q001–Q009 | Responsibility, deployment/service models, consumption, serverless, scaling and reliability | [Cloud concepts path](https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/), [shared responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility), [service types](https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/) |
| Q010–Q011 | Regional/zone boundaries and management scopes | [Regions](https://learn.microsoft.com/en-us/azure/reliability/regions-overview), [architecture path](https://learn.microsoft.com/en-us/training/paths/azure-fundamentals-describe-azure-architecture-services/) |
| Q012–Q015 | Functions, managed hosting, hybrid connectivity and private endpoints | [Compute module](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/), [ExpressRoute](https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction), [VPN Gateway](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways), [private endpoints](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview) |
| Q016–Q019 | File versus object storage, archive, failure boundaries and offline transfer | [Storage module](https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/), [access tiers](https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview), [redundancy](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy), targeted Q016 evidence above |
| Q020–Q021 | SSO versus MFA; scoped resource authorization | [Identity module](https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/), targeted Reader evidence above |
| Q022–Q026 | Estimation, budget alerts, tags, Policy versus RBAC, locks | [Governance path](https://learn.microsoft.com/en-us/training/paths/describe-azure-management-governance/), [budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets), [tags](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources), [Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview), [locks](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources) |
| Q027–Q030 | Hybrid management, declarative provisioning, platform health and app telemetry | [Arc](https://learn.microsoft.com/en-us/azure/azure-arc/overview), [ARM templates](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/overview), [Service Health](https://learn.microsoft.com/en-us/azure/service-health/overview), [Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview) |

The official sources support the underlying concepts; they do not supply or endorse these original questions. No real Azure resources were deployed to test the scenarios. Not every linked lesson or leaf page was audited. Broad source-family review does not establish every product edge case. The primary competency mappings fit the current guide, but each item samples only part of compound objectives such as networking or storage services.

## Adversarial findings and remaining limits

**Novice:** The quick start names the actual input files and provides a starting prompt. Upload limits and unfamiliar terms can still impede entry; domain-by-domain upload and short diagnosis are documented fallbacks. No real beginner onboarding session was observed.

**Experienced developer:** Diagnosis and explanation/application evidence allow the tutor to skip familiar infrastructure concepts. This is a behavioral contract; no live comparison demonstrated that an agent consistently avoids repetition.

**Maintainer:** Source hashes, ordered coverage and stable IDs make the current 57-bullet baseline inspectable. Changed bullet wording still needs editorial interpretation, and previous-version history was not reconstructed. A monitor alert alone cannot map learner evidence safely to a changed objective.

**Azure specialist:** The two corrected ambiguities show why source-linked item review matters. Current keys match the reviewed conceptual sources; human specialist review remains pending. Live product exceptions may require further clarification.

**Education specialist:** Explanations and transfer are required beyond option recognition. Several distractors are intentionally easy and most rubrics are broad. The 30 questions cover 30 primary competencies; 27 competencies have no bank item. Item difficulty and discrimination are uncalibrated, and repeated bank exposure weakens evidence. No learning-gain or retention study was run.

**Agent developer:** JSON and portable instructions avoid a proprietary runtime. Actual file-reading, persistence and retrieval capabilities vary by agent and must be reported. Qualitative fixtures are evaluation plans until model responses are produced and scored.

**Security:** The design keeps external text below the instruction authority, avoids compulsory cloud deployment and excludes learner data from Git by default. These controls reduce obvious exposure but are not evidence of a completed penetration test or live prompt-injection red-team exercise.

**Product:** Curriculum coverage, traceable references, original reasoning tasks, a local evidence ledger and controlled source monitoring are concrete additions to generic chat tutoring. Their educational advantage over an unconfigured model has not been measured. Do not claim a pass guarantee, calibrated readiness probability or demonstrated A/B improvement.
