Não. Há duas responsabilidades para ajustar:

| Situação | Quem cuida? |
| --- | --- |
| Atualizações do sistema operacional convidado de uma VM em **IaaS** | Você, como cliente. |
| Atualizações do sistema operacional da plataforma em **PaaS** | O provedor. Você continua responsável pelo seu código, dados e configurações de acesso. |
| Definir quem pode acessar seus dados em **SaaS** | Sua organização. O provedor opera a aplicação e a infraestrutura, mas não assume todas as decisões sobre permissões dos seus usuários. |

Por exemplo: ao publicar uma aplicação no **Azure App Service**, você não precisa corrigir o sistema operacional da plataforma como faria numa VM. Já em uma aplicação SaaS, se sua equipe der acesso a um documento confidencial para a pessoa errada, essa configuração continua sendo responsabilidade da sua organização.

A ideia é a **responsabilidade compartilhada**: conforme você passa de IaaS para PaaS e SaaS, o provedor assume mais operação; seus dados e decisões de acesso continuam exigindo cuidado. Veja a [explicação oficial da Microsoft](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility).

Para verificar a distinção: uma empresa migrou uma aplicação de uma VM para App Service e um funcionário saiu da empresa, mas ainda tem acesso ao SaaS corporativo. **Quem cuida das atualizações do SO da plataforma e quem deve providenciar a remoção do acesso desse funcionário? Explique o motivo.**