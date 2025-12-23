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


class CrisisPacketGenerator:
    """Generate enhanced crisis packet with emergency phrases and authority messages"""
    
    # Emergency phrases in multiple languages
    EMERGENCY_PHRASES = {
        "English": {
            "help": "I need help!",
            "emergency": "This is an emergency!",
            "hospital": "Take me to the hospital",
            "embassy": "I need to contact my embassy",
            "police": "Call the police",
            "danger": "I am in danger",
        },
        "Spanish": {
            "help": "¡Necesito ayuda!",
            "emergency": "¡Es una emergencia!",
            "hospital": "Lléveme al hospital",
            "embassy": "Necesito contactar mi embajada",
            "police": "Llame a la policía",
            "danger": "Estoy en peligro",
        },
        "French": {
            "help": "J'ai besoin d'aide!",
            "emergency": "C'est une urgence!",
            "hospital": "Emmenez-moi à l'hôpital",
            "embassy": "Je dois contacter mon ambassade",
            "police": "Appelez la police",
            "danger": "Je suis en danger",
        },
        "Arabic": {
            "help": "أحتاج مساعدة!",
            "emergency": "هذه حالة طوارئ!",
            "hospital": "خذني إلى المستشفى",
            "embassy": "أحتاج الاتصال بسفارتي",
            "police": "اتصل بالشرطة",
            "danger": "أنا في خطر",
        },
        "Mandarin": {
            "help": "我需要帮助！",
            "emergency": "这是紧急情况！",
            "hospital": "带我去医院",
            "embassy": "我需要联系我的大使馆",
            "police": "请报警",
            "danger": "我处于危险中",
        },
        "Turkish": {
            "help": "Yardıma ihtiyacım var!",
            "emergency": "Bu bir acil durum!",
            "hospital": "Beni hastaneye götürün",
            "embassy": "Elçiliğimi aramam lazım",
            "police": "Polisi arayın",
            "danger": "Tehlikedeyim",
        },
        "Russian": {
            "help": "Мне нужна помощь!",
            "emergency": "Это экстренная ситуация!",
            "hospital": "Отвезите меня в больницу",
            "embassy": "Мне нужно связаться с посольством",
            "police": "Вызовите полицию",
            "danger": "Я в опасности",
        },
        "Japanese": {
            "help": "助けてください！",
            "emergency": "緊急事態です！",
            "hospital": "病院に連れて行ってください",
            "embassy": "大使館に連絡が必要です",
            "police": "警察を呼んでください",
            "danger": "危険な状況です",
        },
        "Portuguese": {
            "help": "Preciso de ajuda!",
            "emergency": "É uma emergência!",
            "hospital": "Leve-me ao hospital",
            "embassy": "Preciso contactar minha embaixada",
            "police": "Chame a polícia",
            "danger": "Estou em perigo",
        },
        "Hindi": {
            "help": "मुझे मदद चाहिए!",
            "emergency": "यह एक आपातकाल है!",
            "hospital": "मुझे अस्पताल ले जाइए",
            "embassy": "मुझे अपने दूतावास से संपर्क करना है",
            "police": "पुलिस को बुलाइए",
            "danger": "मैं खतरे में हूं",
        },
    }
    
    @staticmethod
    def generate_authority_help_message(user_profile, checklist) -> str:
        """Generate pre-written help message for local authorities"""
        return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                 EMERGENCY ASSISTANCE REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To: Local Authorities / Emergency Services

I am a foreign national requiring emergency assistance.

PERSONAL INFORMATION:
• Name: {user_profile.name}
• Nationality: {user_profile.passport_country}
• Home Country: {user_profile.home_country}
• Current Location: {user_profile.current_location}

EMERGENCY CONTACTS:
{chr(10).join([f"• {c.name} ({c.relationship}): {c.phone}" for c in checklist.emergency_contacts])}

EMBASSY CONTACT:
• {checklist.embassy_info.get('name', 'U.S. Embassy') if checklist.embassy_info else 'Contact embassy'}
• Emergency Line: {checklist.embassy_info.get('emergency', 'See local directory') if checklist.embassy_info else 'See local directory'}

MEDICAL INFORMATION:
• [Add any allergies or medical conditions]

I am following Safe-Passage emergency protocol.
Document verification: SP-{datetime.now().strftime('%Y%m%d')}-AUTH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    @staticmethod
    def generate_crisis_packet(checklist, user_profile) -> str:
        """Generate complete crisis packet with all emergency information"""
        import hashlib
        
        output = []
        
        # Header with verification hash
        doc_hash = hashlib.sha256(
            f"{user_profile.user_id}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12].upper()
        
        output.append("╔" + "═" * 58 + "╗")
        output.append("║" + "SAFE-PASSAGE CRISIS PACKET".center(58) + "║")
        output.append("║" + f"Document ID: SP-{doc_hash}".center(58) + "║")
        output.append("╚" + "═" * 58 + "╝")
        output.append("")
        output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        output.append(f"User: {user_profile.name}")
        output.append(f"Location: {user_profile.current_location}")
        output.append("")
        
        # Authority Help Message
        output.append("=" * 60)
        output.append("SECTION 1: AUTHORITY HELP MESSAGE")
        output.append("=" * 60)
        output.append("(Show this to local authorities if you need assistance)")
        output.append("")
        output.append(CrisisPacketGenerator.generate_authority_help_message(
            user_profile, checklist
        ))
        
        # Emergency Phrases
        output.append("")
        output.append("=" * 60)
        output.append("SECTION 2: CURRENT SITUATION STATUS")
        output.append("=" * 60)
        output.append("")
        output.append(f"📍 Your Location: {user_profile.current_location}")
        if user_profile.exit_fund and user_profile.exit_fund.fallback_destinations:
            fallback = user_profile.exit_fund.fallback_destinations[0]
            output.append(f"✈️ Fallback: {fallback.city}, {fallback.country}")
        output.append(f"💰 Exit Fund: ${user_profile.exit_fund.amount:,.0f} {user_profile.exit_fund.currency}" if user_profile.exit_fund else "No fund configured")
        output.append("")
        
        # Add live network status
        output.append("📡 NETWORK STATUS AT TIME OF GENERATION:")
        output.append("─" * 40)
        
        # Get network status from session state if available
        try:
            import streamlit as st
            if "chaos_simulator" in st.session_state:
                networks = st.session_state.chaos_simulator.get_network_status()
                for network, status in networks.items():
                    icon = "✅" if status == "ONLINE" else "⚠️" if status in ["CONGESTED", "RESTRICTED"] else "❌"
                    output.append(f"   {icon} {network.replace('_', ' ').title()}: {status}")
            else:
                output.append("   🏦 Banking: RESTRICTED (conflict zone)")
                output.append("   💳 ATM: OFFLINE")
                output.append("   ₿ Crypto: ONLINE")
                output.append("   📱 Mobile Money: RESTRICTED")
        except:
            output.append("   🏦 Banking: RESTRICTED (conflict zone)")
            output.append("   💳 ATM: OFFLINE")
            output.append("   ₿ Crypto: ONLINE")
            output.append("   📱 Mobile Money: RESTRICTED")
        
        output.append("")
        output.append("⚠️ RECOMMENDED ACTION:")
        output.append("   Based on current conditions, proceed to fallback destination")
        output.append("   using CRYPTO payout method (banking infrastructure compromised)")
        output.append("")
        
        # Emergency Phrases - prioritize local language
        output.append("")
        output.append("=" * 60)
        output.append("SECTION 3: EMERGENCY PHRASES")
        output.append("=" * 60)
        output.append("")
        
        # Determine priority languages based on user location
        location_country = str(user_profile.current_location).lower()
        priority_languages = ["English"]
        
        if "ukraine" in location_country or "kyiv" in location_country:
            priority_languages = ["Ukrainian", "Russian", "English", "Polish"]
        elif "turkey" in location_country or "istanbul" in location_country:
            priority_languages = ["Turkish", "English", "Arabic"]
        elif "japan" in location_country or "tokyo" in location_country:
            priority_languages = ["Japanese", "English"]
        elif "india" in location_country:
            priority_languages = ["Hindi", "English"]
        
        # Add Ukrainian if not in dictionary
        if "Ukrainian" not in CrisisPacketGenerator.EMERGENCY_PHRASES:
            CrisisPacketGenerator.EMERGENCY_PHRASES["Ukrainian"] = {
                "help": "Мені потрібна допомога!",
                "emergency": "Це надзвичайна ситуація!",
                "hospital": "Відвезіть мене до лікарні",
                "embassy": "Мені потрібно зв'язатися з посольством",
                "police": "Викличте поліцію",
                "danger": "Я в небезпеці",
            }
            CrisisPacketGenerator.EMERGENCY_PHRASES["Polish"] = {
                "help": "Potrzebuję pomocy!",
                "emergency": "To jest nagły wypadek!",
                "hospital": "Zabierzcie mnie do szpitala",
                "embassy": "Muszę skontaktować się z ambasadą",
                "police": "Zadzwońcie na policję",
                "danger": "Jestem w niebezpieczeństwie",
            }
        
        # Show priority languages first, then others
        shown_languages = []
        for language in priority_languages:
            if language in CrisisPacketGenerator.EMERGENCY_PHRASES:
                phrases = CrisisPacketGenerator.EMERGENCY_PHRASES[language]
                output.append(f"【 {language} 】 ★ PRIORITY")
                output.append("-" * 40)
                for key, phrase in phrases.items():
                    output.append(f"  {key.upper():12} → {phrase}")
                output.append("")
                shown_languages.append(language)
        
        output.append("--- Additional Languages ---")
        output.append("")
        for language, phrases in CrisisPacketGenerator.EMERGENCY_PHRASES.items():
            if language not in shown_languages:
                output.append(f"【 {language} 】")
                output.append("-" * 40)
                for key, phrase in phrases.items():
                    output.append(f"  {key.upper():12} → {phrase}")
                output.append("")
        
        # Standard Checklist
        output.append("=" * 60)
        output.append("SECTION 3: EXIT CHECKLIST")
        output.append("=" * 60)
        output.append(ExportManager.export_checklist_text(checklist))
        
        # Offline Route Summary
        output.append("")
        output.append("=" * 60)
        output.append("SECTION 4: OFFLINE ROUTE SUMMARY")
        output.append("=" * 60)
        output.append("")
        
        for i, route in enumerate(checklist.safe_routes, 1):
            output.append(f"ROUTE {i}:")
            output.append(f"  From: {route.from_location}")
            output.append(f"  To:   {route.to_location}")
            output.append(f"  Via:  {route.method.upper()}")
            output.append(f"  Time: {route.estimated_time}")
            output.append(f"  Note: {route.notes}")
            output.append("")
        
        # Document Footer
        output.append("=" * 60)
        output.append("DOCUMENT VERIFICATION")
        output.append("=" * 60)
        output.append(f"Document Hash: {doc_hash}")
        output.append("This document was generated by Safe-Passage Emergency System.")
        output.append("Keep this document accessible offline at all times.")
        output.append("")
        output.append("╔" + "═" * 58 + "╗")
        output.append("║" + "END OF CRISIS PACKET".center(58) + "║")
        output.append("╚" + "═" * 58 + "╝")
        
        return "\n".join(output)
    
    @staticmethod
    def show_crisis_packet_export(checklist, user_profile):
        """Show crisis packet export button"""
        if checklist:
            st.markdown("### 📋 Crisis Packet (Enhanced)")
            st.caption("Complete emergency document with phrases in 10 languages")
            
            packet_content = CrisisPacketGenerator.generate_crisis_packet(
                checklist, user_profile
            )
            
            st.download_button(
                label="📥 Download Crisis Packet",
                data=packet_content.encode("utf-8"),
                file_name=f"crisis_packet_{user_profile.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                type="primary",
                width="stretch",
            )
            
            with st.expander("👁️ Preview Crisis Packet"):
                st.text(packet_content[:2000] + "\n\n... [truncated for preview]")
