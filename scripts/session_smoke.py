"""Reproducible synthetic learner journey with real CLI files; no time travel."""
import argparse
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    from . import tutor
except ImportError:
    import tutor


def execute(output):
    output = Path(output)
    if output.exists():
        raise ValueError("Use a fresh output directory; prior evidence is preserved")
    output.mkdir(parents=True)
    state = output / "session-a/state.json"
    transcript = []

    def call(*args, destination=state):
        command = [sys.executable, str(tutor.ROOT / "scripts/tutor.py"), "--state", str(destination), *args]
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        transcript.append({"arguments": command[2:], "exit_code": result.returncode,
                           "stdout": result.stdout, "stderr": result.stderr})
        if result.returncode:
            raise ValueError(result.stderr)
        return json.loads(result.stdout)

    call("init", "--deadline", (date.today() + timedelta(days=10)).isoformat(), "--minutes", "45",
         "--experience", "SYNTHETIC learner Ana: developer, little Azure", "--language", "pt-BR")
    candidates = call("next")
    # Three proportional diagnostic prompts, answered by a scripted fictional student.
    exchanges = [
        {"mode": "diagnostic", "competency": "AZ900-1.1.2", "question": "smoke-responsibility",
         "tutor": "Numa VM Azure, quem corrige o SO convidado e por quê?",
         "learner": "O cliente: a Microsoft gerencia a infraestrutura física, mas o SO convidado é responsabilidade nossa.",
         "score": 1, "kind": "explanation", "assisted": False, "misconception": ""},
        {"mode": "diagnostic", "competency": "AZ900-1.1.2", "question": "smoke-paas",
         "tutor": "Ao migrar para uma plataforma gerenciada, você continua corrigindo o SO da plataforma?",
         "learner": "Sim, preciso entrar no servidor da plataforma e corrigir o SO.",
         "score": 0, "kind": "explanation", "assisted": False, "misconception": "Customer patches managed PaaS platform OS"},
        {"mode": "diagnostic", "competency": "AZ900-2.2.1", "question": "Q012",
         "tutor": "Na Q012, qual opção você escolheu e qual o motivo?",
         "learner": "B, por chute. Não sei o que Functions faz.",
         "score": 0, "kind": "recall", "assisted": False, "misconception": ""},
        {"mode": "teaching", "competency": "AZ900-1.1.2", "question": "smoke-hint",
         "tutor": "Na plataforma gerenciada, o provedor cuida do SO. Pista: acesso aos seus dados continua com o cliente. Quem configura permissões?",
         "learner": "O cliente configura os acessos aos dados.",
         "score": 1, "kind": "application", "assisted": True, "misconception": ""},
        {"mode": "teaching-transfer", "competency": "AZ900-1.1.2", "question": "smoke-repair",
         "tutor": "Agora um serviço SaaS: quem remove a conta de um ex-funcionário, e quem corrige o SO do serviço?",
         "learner": "Nossa organização remove o acesso do ex-funcionário; o provedor corrige o SO do serviço. Gerenciamento de plataforma não transfere nossas decisões de acesso.",
         "score": 1, "kind": "application", "assisted": False, "misconception": ""}]
    for exchange in exchanges:
        args = ["record", exchange["competency"], "--question", exchange["question"], "--score", str(exchange["score"]),
                "--kind", exchange["kind"], "--evidence", "SYNTHETIC student: " + exchange["learner"],
                "--misconception", exchange["misconception"]]
        if exchange["assisted"]:
            args.append("--assisted")
        exchange["record_result"] = call(*args)
    pending, reviews = call("pending"), call("reviews")
    exported = output / "portable.json"
    call("export", str(exported.resolve()))
    restored = output / "session-b/state.json"
    call("import", str(exported.resolve()), destination=restored)
    assert tutor.read(state) == tutor.read(restored)
    resumed = call("next", destination=restored)
    assert resumed == call("next")
    # The chatbot path uses exactly the documented state-v1 shape, without a checksum.
    manual = output / "manual-chatbot.json"
    tutor.atomic_write(manual, tutor.read(state))
    chatbot = output / "session-c/state.json"
    call("import", str(manual.resolve()), destination=chatbot)
    assert tutor.read(chatbot) == tutor.read(state)
    statuses = call("status", destination=restored)
    assert all(s["status"] != "demonstrated" for s in statuses.values())
    report = {"date": date.today().isoformat(), "identity": "Fictional scripted learner; not a model efficacy trial",
              "clock": "Actual local date, no simulated delayed review", "diagnostic_candidates": candidates,
              "exchanges": exchanges, "pending_count": len(pending), "due_reviews": reviews,
              "resumed_next": resumed, "roundtrip_equal": True, "manual_handoff_import_equal": True,
              "resume": "Continue shared responsibility practice; hinted recovery and same-day transfer do not demonstrate mastery. Other objectives remain unassessed.",
              "commands": transcript}
    tutor.atomic_write(output / "report.json", report)
    return {"report": str(output / "report.json"), "events": 5, "roundtrip_equal": True, "manual_handoff_import_equal": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(execute(args.output), ensure_ascii=False))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
