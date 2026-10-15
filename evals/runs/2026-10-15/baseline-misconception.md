Não. As duas afirmações precisam de ajuste:

| Modelo | Quem atualiza o sistema operacional? | Quem decide as permissões dos seus usuários? |
|---|---|---|
| **IaaS**, como uma VM do Azure | Você atualiza o SO convidado. | Você/sua organização. |
| **PaaS** | A Microsoft atualiza o SO da plataforma gerenciada. | Você/sua organização. |
| **SaaS** | O provedor gerencia o SO e a aplicação. | Você/sua organização continua responsável por conceder e revisar os acessos. |

No SaaS, a Microsoft pode fornecer os mecanismos de identidade e acesso, mas isso não significa que ela decida quem deve acessar os seus dados. Seus dados e suas decisões de acesso continuam sendo sua responsabilidade. Veja o [modelo de responsabilidade compartilhada da Microsoft](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility).

Para fixar: uma pessoa sai da empresa que usa um SaaS. Quem deve garantir que o acesso dela seja removido?
