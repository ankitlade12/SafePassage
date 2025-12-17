"""
Simulated Payout Systems - Phase 3
Realistic simulation of crypto, wire transfer, and cash pickup
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
from models import PayoutMethod
import random
import time


@dataclass
class PayoutTransaction:
    """Payout transaction record"""
    transaction_id: str
    method: PayoutMethod
    amount: float
    currency: str
    status: str  # "pending", "processing", "completed", "failed"
    initiated_at: datetime
    completed_at: Optional[datetime] = None
    confirmation_code: Optional[str] = None
    recipient_address: Optional[str] = None
    estimated_arrival: Optional[datetime] = None
    
    def get_progress_percentage(self) -> int:
        """Calculate progress percentage"""
        if self.status == "completed":
            return 100
        elif self.status == "processing":
            return 60
        elif self.status == "pending":
            return 20
        else:
            return 0


class CryptoWalletSimulator:
    """Simulate crypto wallet payout"""
    
    def __init__(self):
        self.network = "Ethereum"
        self.avg_confirmation_time = 15  # minutes
    
    def initiate_payout(self, amount: float, currency: str, wallet_address: str) -> PayoutTransaction:
        """Initiate crypto payout"""
        
        # Generate realistic transaction ID
        tx_id = f"0x{random.randbytes(32).hex()}"
        
        transaction = PayoutTransaction(
            transaction_id=tx_id,
            method=PayoutMethod.CRYPTO_WALLET,
            amount=amount,
            currency=currency,
            status="pending",
            initiated_at=datetime.now(),
            recipient_address=wallet_address,
            estimated_arrival=datetime.now() + timedelta(minutes=self.avg_confirmation_time)
        )
        
        return transaction
    
    def check_status(self, transaction: PayoutTransaction) -> PayoutTransaction:
        """Check transaction status"""
        
        elapsed = (datetime.now() - transaction.initiated_at).total_seconds() / 60
        
        if elapsed < 2:
            transaction.status = "pending"
        elif elapsed < 10:
            transaction.status = "processing"
            transaction.confirmation_code = f"Confirmations: {int(elapsed)}/12"
        else:
            transaction.status = "completed"
            transaction.completed_at = datetime.now()
            transaction.confirmation_code = "12/12 Confirmations"
        
        return transaction
    
    def get_wallet_balance(self, wallet_address: str) -> dict:
        """Get simulated wallet balance"""
        return {
            "address": wallet_address,
            "balance": 0.0,
            "pending": 0.0,
            "currency": "USDC"
        }


class WireTransferSimulator:
    """Simulate wire transfer payout"""
    
    def __init__(self):
        self.processing_days = 2  # 2-3 business days
    
    def initiate_payout(self, amount: float, currency: str, 
                       account_number: str, routing_number: str) -> PayoutTransaction:
        """Initiate wire transfer"""
        
        # Generate reference number
        ref_number = f"WIRE{random.randint(100000, 999999)}"
        
        transaction = PayoutTransaction(
            transaction_id=ref_number,
            method=PayoutMethod.WIRE_TRANSFER,
            amount=amount,
            currency=currency,
            status="pending",
            initiated_at=datetime.now(),
            confirmation_code=ref_number,
            estimated_arrival=datetime.now() + timedelta(days=self.processing_days)
        )
        
        return transaction
    
    def check_status(self, transaction: PayoutTransaction) -> PayoutTransaction:
        """Check wire transfer status"""
        
        elapsed_hours = (datetime.now() - transaction.initiated_at).total_seconds() / 3600
        
        if elapsed_hours < 1:
            transaction.status = "pending"
        elif elapsed_hours < 48:
            transaction.status = "processing"
        else:
            transaction.status = "completed"
            transaction.completed_at = datetime.now()
        
        return transaction


class CashPickupSimulator:
    """Simulate cash pickup payout (Western Union style)"""
    
    def __init__(self):
        self.avg_availability = 4  # hours
        self.locations = [
            "Western Union - Main Street Branch",
            "MoneyGram - Airport Location",
            "Ria Money Transfer - Downtown"
        ]
    
    def initiate_payout(self, amount: float, currency: str, 
                       recipient_name: str, recipient_phone: str) -> PayoutTransaction:
        """Initiate cash pickup"""
        
        # Generate MTCN (Money Transfer Control Number)
        mtcn = f"{random.randint(1000000000, 9999999999)}"
        
        transaction = PayoutTransaction(
            transaction_id=mtcn,
            method=PayoutMethod.CASH_PICKUP,
            amount=amount,
            currency=currency,
            status="pending",
            initiated_at=datetime.now(),
            confirmation_code=f"MTCN: {mtcn}",
            estimated_arrival=datetime.now() + timedelta(hours=self.avg_availability)
        )
        
        return transaction
    
    def check_status(self, transaction: PayoutTransaction) -> PayoutTransaction:
        """Check cash pickup status"""
        
        elapsed_hours = (datetime.now() - transaction.initiated_at).total_seconds() / 3600
        
        if elapsed_hours < 0.5:
            transaction.status = "pending"
        elif elapsed_hours < 3:
            transaction.status = "processing"
        else:
            transaction.status = "completed"
            transaction.completed_at = datetime.now()
        
        return transaction
    
    def get_pickup_locations(self, city: str) -> list:
        """Get available pickup locations"""
        return self.locations


class MobileMoneySimulator:
    """Simulate mobile money payout (M-Pesa style)"""
    
    def __init__(self):
        self.avg_delivery = 30  # minutes
    
    def initiate_payout(self, amount: float, currency: str, 
                       phone_number: str) -> PayoutTransaction:
        """Initiate mobile money transfer"""
        
        # Generate transaction ID
        tx_id = f"MM{random.randint(100000000, 999999999)}"
        
        transaction = PayoutTransaction(
            transaction_id=tx_id,
            method=PayoutMethod.MOBILE_MONEY,
            amount=amount,
            currency=currency,
            status="pending",
            initiated_at=datetime.now(),
            recipient_address=phone_number,
            confirmation_code=tx_id,
            estimated_arrival=datetime.now() + timedelta(minutes=self.avg_delivery)
        )
        
        return transaction
    
    def check_status(self, transaction: PayoutTransaction) -> PayoutTransaction:
        """Check mobile money status"""
        
        elapsed_minutes = (datetime.now() - transaction.initiated_at).total_seconds() / 60
        
        if elapsed_minutes < 5:
            transaction.status = "pending"
        elif elapsed_minutes < 20:
            transaction.status = "processing"
        else:
            transaction.status = "completed"
            transaction.completed_at = datetime.now()
        
        return transaction


class PayoutOrchestrator:
    """Orchestrate all payout methods"""
    
    def __init__(self):
        self.crypto = CryptoWalletSimulator()
        self.wire = WireTransferSimulator()
        self.cash = CashPickupSimulator()
        self.mobile = MobileMoneySimulator()
    
    def initiate_payout(self, method: PayoutMethod, amount: float, 
                       currency: str, **kwargs) -> PayoutTransaction:
        """Initiate payout using selected method"""
        
        if method == PayoutMethod.CRYPTO_WALLET:
            wallet_address = kwargs.get('wallet_address', '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb')
            return self.crypto.initiate_payout(amount, currency, wallet_address)
        
        elif method == PayoutMethod.WIRE_TRANSFER:
            account = kwargs.get('account_number', '****1234')
            routing = kwargs.get('routing_number', '****5678')
            return self.wire.initiate_payout(amount, currency, account, routing)
        
        elif method == PayoutMethod.CASH_PICKUP:
            name = kwargs.get('recipient_name', 'User')
            phone = kwargs.get('recipient_phone', '+1-555-0100')
            return self.cash.initiate_payout(amount, currency, name, phone)
        
        elif method == PayoutMethod.MOBILE_MONEY:
            phone = kwargs.get('phone_number', '+254-700-000000')
            return self.mobile.initiate_payout(amount, currency, phone)
        
        else:
            raise ValueError(f"Unsupported payout method: {method}")
    
    def check_status(self, transaction: PayoutTransaction) -> PayoutTransaction:
        """Check status of any transaction"""
        
        if transaction.method == PayoutMethod.CRYPTO_WALLET:
            return self.crypto.check_status(transaction)
        elif transaction.method == PayoutMethod.WIRE_TRANSFER:
            return self.wire.check_status(transaction)
        elif transaction.method == PayoutMethod.CASH_PICKUP:
            return self.cash.check_status(transaction)
        elif transaction.method == PayoutMethod.MOBILE_MONEY:
            return self.mobile.check_status(transaction)
        
        return transaction
    
    def get_method_details(self, method: PayoutMethod) -> dict:
        """Get details about payout method"""
        
        details = {
            PayoutMethod.CRYPTO_WALLET: {
                "name": "Crypto Wallet (USDC)",
                "eta": "15 minutes",
                "fee": "$2.50",
                "network": "Ethereum",
                "confirmations_required": 12
            },
            PayoutMethod.WIRE_TRANSFER: {
                "name": "Wire Transfer",
                "eta": "2-3 business days",
                "fee": "$25.00",
                "networks": ["SWIFT", "ACH"],
                "limits": "$1,000 - $50,000"
            },
            PayoutMethod.CASH_PICKUP: {
                "name": "Cash Pickup",
                "eta": "2-4 hours",
                "fee": "$10.00",
                "partners": ["Western Union", "MoneyGram", "Ria"],
                "locations": "50,000+ worldwide"
            },
            PayoutMethod.MOBILE_MONEY: {
                "name": "Mobile Money",
                "eta": "30 minutes",
                "fee": "$1.00",
                "networks": ["M-Pesa", "MTN Mobile Money"],
                "regions": ["Africa", "Asia"]
            }
        }
        
        return details.get(method, {})
