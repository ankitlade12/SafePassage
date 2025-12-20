"""
Export Features
PDF and JSON export for exit checklists and audit trails
"""

from models import ExitChecklist, EmergencyActivation
import streamlit as st
from datetime import datetime
import json


class ExportManager:
    """Manage exports for checklists and audit trails"""

    @staticmethod
    def export_checklist_text(checklist: ExitChecklist) -> str:
        """Export checklist as formatted text"""

        output = []
        output.append("=" * 60)
        output.append("EMERGENCY EXIT CHECKLIST")
        output.append("=" * 60)
        output.append(
            f"\nGenerated: {checklist.generated_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        output.append(f"Location: {checklist.location}")
        output.append("\n" + "=" * 60)

        # Critical items
        output.append("\n🔴 CRITICAL ACTIONS (DO FIRST):")
        output.append("-" * 60)
        critical = checklist.get_critical_items()
        for i, item in enumerate(critical, 1):
            output.append(f"\n{i}. {item.title}")
            output.append(f"   {item.description}")

        # Additional items
        output.append("\n\n📌 ADDITIONAL STEPS:")
        output.append("-" * 60)
        additional = [item for item in checklist.items if item.priority > 2]
        for i, item in enumerate(additional, 1):
            output.append(f"\n{i}. {item.title}")
            output.append(f"   {item.description}")

        # Safe routes
        output.append("\n\n🛫 SAFE ROUTES:")
        output.append("-" * 60)
        for route in checklist.safe_routes:
            output.append(
                f"\n{route.method.upper()}: {route.from_location} → {route.to_location}"
            )
            output.append(f"Estimated time: {route.estimated_time}")
            output.append(f"Notes: {route.notes}")

        # Money access
        output.append("\n\n💵 MONEY ACCESS STEPS:")
        output.append("-" * 60)
        for i, step in enumerate(checklist.money_access_steps, 1):
            output.append(f"{i}. {step}")

        # Embassy info
        if checklist.embassy_info:
            output.append("\n\n🏛️ EMBASSY INFORMATION:")
            output.append("-" * 60)
            output.append(f"Name: {checklist.embassy_info.get('name')}")
            if checklist.embassy_info.get("address"):
                output.append(f"Address: {checklist.embassy_info.get('address')}")
            output.append(f"Phone: {checklist.embassy_info.get('phone')}")
            output.append(f"Emergency: {checklist.embassy_info.get('emergency')}")

        # Emergency contacts
        output.append("\n\n📞 EMERGENCY CONTACTS:")
        output.append("-" * 60)
        for contact in checklist.emergency_contacts:
            output.append(f"\n{contact.name} ({contact.relationship})")
            output.append(f"Phone: {contact.phone}")
            output.append(f"Email: {contact.email}")

        output.append("\n" + "=" * 60)
        output.append("END OF CHECKLIST")
        output.append("=" * 60)

        return "\n".join(output)

    @staticmethod
    def export_audit_trail_json(activation: EmergencyActivation) -> str:
        """Export audit trail as JSON"""

        audit_data = {
            "activation_id": activation.activation_id,
            "user_id": activation.user_id,
            "timestamp": activation.timestamp.isoformat(),
            "trigger_alert": activation.triggered_by_alert,
            "payout": {
                "method": activation.payout_method.value,
                "amount": activation.payout_amount,
                "currency": activation.payout_currency,
                "status": activation.status,
            },
            "completion_time": activation.completion_time.isoformat()
            if activation.completion_time
            else None,
            "notes": activation.notes,
            "generated_at": datetime.now().isoformat(),
        }

        return json.dumps(audit_data, indent=2)

    @staticmethod
    def create_download_link(content: str, filename: str, label: str) -> str:
        """Create download link for content"""
        import base64

        b64 = base64.b64encode(content.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'
        return href


class PDFExporter:
    """Export exit checklist to PDF"""

    @staticmethod
    def create_simple_pdf(checklist, user_profile):
        """Create simple text-based PDF"""
        # Use existing text export and convert to downloadable format
        text_content = ExportManager.export_checklist_text(checklist)

        return text_content.encode("utf-8")

    @staticmethod
    def show_pdf_export_button(checklist, user_profile):
        """Show PDF export button"""
        if checklist:
            st.markdown("### 📄 Export Checklist")

            col1, col2 = st.columns(2)

            with col1:
                # Text export
                text_content = PDFExporter.create_simple_pdf(checklist, user_profile)
                st.download_button(
                    label="📥 Download as Text",
                    data=text_content,
                    file_name=f"exit_checklist_{user_profile.name.replace(' ', '_')}.txt",
                    mime="text/plain",
                    width="stretch",
                )

            with col2:
                # JSON export (for backup)
                import json

                checklist_data = {
                    "user": user_profile.name,
                    "location": str(checklist.location),
                    "generated": checklist.generated_at.isoformat(),
                    "critical_items": [
                        {"title": item.title, "description": item.description}
                        for item in checklist.get_critical_items()
                    ],
                    "routes": [
                        {
                            "method": route.method,
                            "from": str(route.from_location),
                            "to": str(route.to_location),
                            "time": route.estimated_time,
                        }
                        for route in checklist.safe_routes
                    ],
                }

                st.download_button(
                    label="📥 Download as JSON",
                    data=json.dumps(checklist_data, indent=2),
                    file_name=f"exit_checklist_{user_profile.name.replace(' ', '_')}.json",
                    mime="application/json",
                    width="stretch",
                )
