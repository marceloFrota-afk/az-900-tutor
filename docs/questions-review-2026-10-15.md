# Question bank expansion and author review — 2026-10-15

Evaluator: the question-authoring AI agent working on this maintenance task. This is an author self-review, **not independent editorial review** of the new material, a human Azure SME review, or a learner evaluation. The inherited Q001–Q030 second-agent review is recorded separately in bank provenance. No real learner records were used.

## Scope and result

The author read all existing prompts, options, keys, rubrics, distractor feedback and primary mappings, then added 35 original scenarios. Q001–Q030 keep their IDs, contents and primary competency mappings. Q031–Q057 cover the 27 formerly unassessed primary competencies. Q058–Q065 add transfer variants. The bank now has 65 items across all 57 competencies: D1 17, D2 30, D3 18. Seven items remain multiple choice; all 35 additions require explained application. New prompts use explicit item-specific full-credit criteria and 0–3 partial/no-credit guidance.

Author checks found no required semantic correction to the inherited 30 questions. The expansion explicitly avoids several common overstatements: a regional pair does not replicate every application; a public IP is not mandatory for a VM; Premium storage accounts do not support every service; Entra ID is not a conventional domain controller; being invited/authenticated does not confer unrestricted authorization; budgets do not stop all consumption; redundancy is not historical recovery; a recommendation does not automatically remediate a resource. These are editorial judgments pending independent review.

## Official source inspection

The author fetched the following official module families and relevant conceptual unit pages through web tools on 2026-10-15. Sources inform the underlying concepts; the prompts are original scenarios. No module assessment questions were requested or reproduced. Each new item's `source_urls` identifies its conceptual basis and `verified_at` records today's inspection. Module summaries sometimes include material outside the approved exam outline; additions follow the local 57-competency mapping rather than treating every training objective as an exam objective.

| Items | Conceptual sources inspected |
| --- | --- |
| Q031–Q033 | [Cloud computing](https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/), [Spot VMs](https://learn.microsoft.com/en-us/azure/virtual-machines/spot-vms), [Reservations](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations) |
| Q034–Q036, Q058, Q064 | [Cloud benefits](https://learn.microsoft.com/en-us/training/modules/describe-benefits-use-cloud-services/), [Service types](https://learn.microsoft.com/en-us/training/modules/describe-cloud-service-types/) |
| Q037–Q041, Q065 | [Architecture](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/), [Region pairs and nonpaired regions](https://learn.microsoft.com/en-us/azure/reliability/regions-paired) |
| Q042–Q043 | [VMs](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/2-virtual-machines), [Virtual Desktop](https://learn.microsoft.com/en-us/training/modules/describe-azure-compute-networking-services/4-virtual-desktop) |
| Q044–Q045, Q063 | [Storage accounts](https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/2-accounts), [File movement](https://learn.microsoft.com/en-us/training/modules/describe-azure-storage-services/7-identify-azure-file-movement-options), [Data protection](https://learn.microsoft.com/en-us/azure/storage/blobs/data-protection-overview) |
| Q046–Q051, Q059 | [Identity/security](https://learn.microsoft.com/en-us/training/modules/describe-azure-identity-access-security/), [Entra Domain Services](https://learn.microsoft.com/en-us/entra/identity/domain-services/overview), [Defender for Cloud](https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction), [RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview) |
| Q052, Q061 | [Cost factors](https://learn.microsoft.com/en-us/training/modules/describe-cost-management-azure/2-describe-factors-affect-costs-azure), [Budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets) |
| Q053, Q060 | [Purview](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-azure-for-governance-compliance/2-describe-purpose-microsoft-purview), [Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview), [Locks](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources) |
| Q054–Q056 | [Interaction tools](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/2-describe-interacting-azure), [ARM templates](https://learn.microsoft.com/en-us/training/modules/describe-features-tools-manage-deploy-azure-resources/4-describe-azure-resource-manager-azure-arm-templates) |
| Q057, Q062 | [Advisor](https://learn.microsoft.com/en-us/training/modules/describe-monitoring-tools-azure/2-describe-purpose-of-azure-advisor), [Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview) |

A VNet overview fetch returned a cache miss; it was not used as verified support. Several official documentation pages display a generic sign-in notice while still exposing the conceptual article body; inspection used the body, without accessing a private Azure tenant. Source verification does not imply that every leaf of the original 30 source paths was re-read or any Azure deployment was tested.

## Verification and remaining limitations

The committed coverage tests compare the complete primary competency set with the curriculum, protect Q001–Q030 mappings, check original/source/rubric metadata and coverage counts, and require distinct transfer variants. A missing-competency fixture retains all three domains and must be rejected by the repository validator. Run the full documented validation after integration; parent-agent changes to the validator enforce that last contract. This report does not claim that automated checks evaluate the educational quality of the questions.

The additions are marked independent review pending in item metadata. Independent review must examine the final prompts, keys, criteria and mappings before changing that status. Human subject-matter review, learner trials, translation review, empirical difficulty, item discrimination, fresh delayed exercises and pass prediction remain unvalidated. Broad primary coverage is not full sub-concept coverage or evidence that a learner has mastered all 57 competencies.
