"""
Smart Liquidity Oracle & Network Simulator
Determines the optimal payout method based on real-time risk, network conditions, and user urgency.
"""

import random
from enum import Enum
from dataclasses import dataclass
from typing import List
from models import PayoutMethod, Location


class NetworkStatus(Enum):
    ONLINE = "ONLINE"
    CONGESTED = "CONGESTED"
    OFFLINE = "OFFLINE"
    RESTRICTED = "RESTRICTED"  # e.g., capital controls


@dataclass
class NetworkCondition:
    status: NetworkStatus
    latency_ms: int
    fee_multiplier: float
    success_rate: float
    message: str


class NetworkStatusSimulator:
    """Simulates real-world financial network conditions based on location risk"""

    @staticmethod
    def get_network_status(
        method: PayoutMethod, risk_level: int, location: Location
    ) -> NetworkCondition:
        """
        Simulate network status based on risk level.
        High risk (7+) increases chance of banking failures and capital controls.
        """
        # Default healthy state
        status = NetworkStatus.ONLINE
        latency = 100
        fee_mult = 1.0
        success_rate = 0.99
        message = "Network optimal"

        # Simulation logic
        rng = random.random()

        if risk_level >= 8:
            # Crisis scenario: High chance of banking failure
            if method in [PayoutMethod.WIRE_TRANSFER, PayoutMethod.MOBILE_MONEY]:
                if rng < 0.7:
                    status = NetworkStatus.OFFLINE
                    success_rate = 0.0
                    message = "Banks closed due to civil unrest"
                elif rng < 0.9:
                    status = NetworkStatus.RESTRICTED
                    fee_mult = 2.0
                    message = "Capital controls active - delays expected"

            # Crypto might be congested but usually works
            elif method == PayoutMethod.CRYPTO_WALLET:
                if rng < 0.3:
                    status = NetworkStatus.CONGESTED
                    latency = 5000
                    fee_mult = 3.0
                    message = "Network congested - high gas fees"

        elif risk_level >= 5:
            # Moderate risk: Occasional disruptions
            if method == PayoutMethod.CASH_PICKUP and rng < 0.4:
                status = NetworkStatus.RESTRICTED
                message = "Limited agent availability"

        return NetworkCondition(status, latency, fee_mult, success_rate, message)


@dataclass
class PayoutRecommendation:
    method: PayoutMethod
    match_score: int  # 0-100
    network_condition: NetworkCondition
    estimated_time: str
    estimated_fee: str
    badges: List[str]  # ["Fastest", "Cheapest", "Safest"]
    reason: str


class LiquidityOracle:
    """
    The Brain: Scores and ranks payout methods.
    """

    # Base characteristics (generic)
    METHOD_Traits = {
        PayoutMethod.CRYPTO_WALLET: {
            "speed": 9,
            "reliability": 8,
            "cost": 7,
            "privacy": 10,
        },
        PayoutMethod.WIRE_TRANSFER: {
            "speed": 3,
            "reliability": 9,
            "cost": 5,
            "privacy": 6,
        },
        PayoutMethod.CASH_PICKUP: {
            "speed": 7,
            "reliability": 6,
            "cost": 4,
            "privacy": 8,
        },
        PayoutMethod.MOBILE_MONEY: {
            "speed": 8,
            "reliability": 9,
            "cost": 9,
            "privacy": 7,
        },
    }

    @staticmethod
    def get_recommendations(
        user_profile, risk_level: int
    ) -> List[PayoutRecommendation]:
        """
        Rank payout methods for the user context.
        """
        recommendations = []

        # 1. Determine Weights based on Context
        if risk_level >= 7:
            # Crisis: Speed and Reliability are king. Cost doesn't matter.
            weights = {"speed": 0.50, "reliability": 0.40, "cost": 0.10}
        else:
            # Normal: Cost is more important
            weights = {"speed": 0.30, "reliability": 0.30, "cost": 0.40}

        location = user_profile.current_location
        available_methods = (
            user_profile.exit_fund.payout_methods
            if user_profile.exit_fund
            else list(PayoutMethod)
        )

        for method in available_methods:
            # Get simulated real-time network interactions
            net_cond = NetworkStatusSimulator.get_network_status(
                method, risk_level, location
            )

            # If offline, score is 0
            if net_cond.status == NetworkStatus.OFFLINE:
                reco = PayoutRecommendation(
                    method=method,
                    match_score=0,
                    network_condition=net_cond,
                    estimated_time="N/A",
                    estimated_fee="N/A",
                    badges=["UNAVAILABLE"],
                    reason=f"Unavailable: {net_cond.message}",
                )
                recommendations.append(reco)
                continue

            # Calculate Score
            traits = LiquidityOracle.METHOD_Traits.get(
                method, {"speed": 5, "reliability": 5, "cost": 5}
            )

            # Adjust traits based on network condition
            adj_speed = traits["speed"]
            if net_cond.status == NetworkStatus.CONGESTED:
                adj_speed *= 0.5

            # Score formula
            raw_score = (
                (adj_speed * weights["speed"])
                + (traits["reliability"] * weights["reliability"])
                + (traits["cost"] * weights["cost"])
            ) * 10  # Scale to 0-100

            # Penalize for restricted status
            if net_cond.status == NetworkStatus.RESTRICTED:
                raw_score *= 0.7

            score = int(min(100, max(0, raw_score)))

            # Determine Badges
            badges = []
            if net_cond.status == NetworkStatus.ONLINE:
                if method == PayoutMethod.CRYPTO_WALLET:
                    badges.append("⚡ Instant")
                if method == PayoutMethod.MOBILE_MONEY:
                    badges.append("💰 Low Fee")
            if score > 90:
                badges.append("🏆 Recommended")

            # Estimated strings
            time_str = "Unknown"
            if method == PayoutMethod.CRYPTO_WALLET:
                time_str = (
                    "~10 mins"
                    if net_cond.status == NetworkStatus.ONLINE
                    else "> 1 hour"
                )
            elif method == PayoutMethod.WIRE_TRANSFER:
                time_str = "1-3 days"
            elif method == PayoutMethod.CASH_PICKUP:
                time_str = "2-4 hours"
            elif method == PayoutMethod.MOBILE_MONEY:
                time_str = "30 mins"

            reco = PayoutRecommendation(
                method=method,
                match_score=score,
                network_condition=net_cond,
                estimated_time=time_str,
                estimated_fee=f"${5 * net_cond.fee_multiplier:.2f}",  # Simplified fee logic
                badges=badges,
                reason=net_cond.message,
            )
            recommendations.append(reco)

        # Sort by score descending
        recommendations.sort(key=lambda x: x.match_score, reverse=True)

        # Add "Fastest" and "Safest" badges relative to the set
        if recommendations and recommendations[0].match_score > 0:
            recommendations[0].badges.append("⭐ Best Match")

        return recommendations
