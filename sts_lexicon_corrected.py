
"""
Lexique STS corrigé - Grille officielle structurée
Ethereum Foundation Discursive Analysis

9 catégories STS (analytico-théoriques) selon la grille méthodologique
établie pour l'analyse socio-technique du corpus EF
"""

# 🧭 GRILLE STS OFFICIELLE - 9 CATÉGORIES STRUCTURÉES

STS_LEXICON_CORRECTED = {
    
    # 1. PROTOCOLAIRE - Règles de fonctionnement blockchain
    'protocolaire': {
        'eip', 'eips', 'hardfork', 'fork', 'consensus', 'upgrade', 'protocol', 
        'specification', 'standard', 'improvement', 'proposal', 'ethereum', 
        'beacon', 'merge', 'pos', 'pow', 'casper', 'finality', 'epoch', 
        'slot', 'validator', 'attestation', 'committee', 'sync', 'checkpoint', 
        'rules', 'hard', 'soft', 'activation', 'implementation'
    },
    
    # 2. INFRASTRUCTUREL - Couches techniques de support
    'infrastructurel': {
        'network', 'scaling', 'layer', 'rollup', 'rollups', 'optimistic', 
        'arbitrum', 'optimism', 'zk', 'zkrollup', 'polygon', 'shard', 
        'sharding', 'shards', 'execution', 'consensus', 'beacon', 'chain', 
        'block', 'blockchain', 'node', 'nodes', 'client', 'clients', 'peer', 
        'infrastructure', 'architecture', 'latency', 'throughput', 'performance', 
        'capacity', 'bandwidth', 'synchronization'
    },
    
    # 3. GOUVERNANCE - Gestion, validation, prise de décision
    'gouvernance': {
        'staking', 'stake', 'staker', 'slashing', 'validator', 'validators', 
        'delegate', 'delegation', 'governance', 'dao', 'vote', 'voting', 
        'proposal', 'decision', 'foundation', 'board', 'community', 
        'coordination', 'stakeholder', 'participant', 'member', 'contributor', 
        'committee', 'council', 'democratic', 'participation', 'funding', 
        'grant', 'treasury', 'budget'
    },
    
    # 4. SÉCURITÉ - Vulnérabilités, audits, cryptographie
    'sécurité': {
        'security', 'vulnerability', 'audit', 'bug', 'exploit', 'attack', 
        'threat', 'risk', 'cryptography', 'encryption', 'signature', 
        'verification', 'proof', 'zk', 'zero', 'knowledge', 'formal', 
        'safety', 'secure', 'trust', 'trustless', 'immutable', 'tamper', 
        'resistant', 'robust', 'authentication', 'authorization', 'privacy'
    },
    
    # 5. USAGES - Applications concrètes, interfaces utilisateur
    'usages': {
        'wallet', 'wallets', 'interface', 'user', 'experience', 'usability', 
        'accessibility', 'dapp', 'dapps', 'application', 'applications', 
        'service', 'platform', 'adoption', 'mainstream', 'enterprise', 
        'business', 'frontend', 'backend', 'mobile', 'web', 'browser', 
        'metamask', 'etherscan', 'tools', 'tooling', 'ux', 'ui'
    },
    
    # 6. RECHERCHE - Production de savoirs scientifiques
    'recherche': {
        'research', 'paper', 'academic', 'study', 'analysis', 'theory', 
        'theoretical', 'model', 'modeling', 'simulation', 'experiment', 
        'formal', 'mathematics', 'cryptographic', 'algorithm', 'optimization', 
        'design', 'specification', 'whitepaper', 'yellowpaper', 'documentation', 
        'technical', 'science', 'methodology', 'empirical'
    },
    
    # 7. DÉVELOPPEMENT - Outils et pratiques de développement
    'développement': {
        'solidity', 'vyper', 'foundry', 'hardhat', 'truffle', 'remix', 
        'compiler', 'development', 'developer', 'coding', 'programming', 
        'software', 'code', 'implementation', 'deployment', 'testing', 
        'debugging', 'github', 'repository', 'commit', 'pull', 'request', 
        'issue', 'feature', 'api', 'sdk', 'library', 'framework', 'toolchain', 
        'ide', 'environment', 'build'
    },
    
    # 8. DEFI/FINANCE - Vocabulaire financier et DeFi
    'defi_finance': {
        'defi', 'amm', 'mev', 'liquidity', 'flashloan', 'yield', 'farming', 
        'swap', 'uniswap', 'compound', 'aave', 'maker', 'dai', 'usdc', 
        'token', 'tokens', 'erc20', 'erc721', 'nft', 'nfts', 'market', 
        'trading', 'exchange', 'price', 'value', 'economic', 'economy', 
        'financial', 'monetary', 'currency', 'eth', 'ether', 'gas', 'fee', 
        'fees', 'cost', 'incentive', 'reward', 'stake', 'pool'
    },
    
    # 9. DISCOURS/VISION - Concepts stratégiques et philosophiques
    'discours_vision': {
        'decentralized', 'decentralization', 'centralized', 'trustless', 
        'permissionless', 'censorship', 'resistant', 'open', 'transparent', 
        'immutable', 'autonomous', 'sovereignty', 'freedom', 'innovation', 
        'disruption', 'transformation', 'future', 'vision', 'philosophy', 
        'values', 'principles', 'ethos', 'mission', 'scalable', 'sustainable', 
        'inclusive', 'accessible', 'global', 'universal', 'revolution'
    }
}

# 🏷️ Catégories indigènes EF (selon métadonnées extraction)
EF_INDIGENOUS_CATEGORIES_CORRECTED = {
    'research_development': {
        'research', 'development', 'experimental', 'prototype', 'proof', 
        'concept', 'design', 'specification', 'academic', 'paper', 'study', 
        'analysis', 'investigation', 'exploration'
    },
    
    'updates_upgrades': {
        'update', 'upgrade', 'fork', 'hardfork', 'merge', 'transition', 
        'migration', 'announcement', 'release', 'version', 'changelog', 
        'improvement', 'patch', 'fix'
    },
    
    'events_community': {
        'devcon', 'conference', 'hackathon', 'meetup', 'event', 'community', 
        'workshop', 'talk', 'presentation', 'gathering', 'summit', 'fellowship'
    },
    
    'security': {
        'security', 'vulnerability', 'audit', 'bug', 'bounty', 'exploit', 
        'patch', 'fix', 'advisory', 'disclosure', 'responsible', 'review'
    },
    
    'staking_merge': {
        'staking', 'stake', 'validator', 'beacon', 'merge', 'pos', 'proof', 
        'transition', 'consensus', 'finality', 'slashing', 'attestation'
    },
    
    'layer2_scaling': {
        'layer', 'scaling', 'rollup', 'rollups', 'optimistic', 'zk', 
        'arbitrum', 'optimism', 'polygon', 'shard', 'sharding', 'throughput'
    },
    
    'wallet_ux': {
        'wallet', 'interface', 'user', 'experience', 'usability', 'mobile', 
        'web', 'browser', 'frontend', 'design', 'accessibility', 'ui', 'ux'
    },
    
    'ecosystem_adoption': {
        'ecosystem', 'adoption', 'partnership', 'integration', 'enterprise', 
        'business', 'industry', 'mainstream', 'education', 'outreach'
    },
    
    'governance_coordination': {
        'governance', 'coordination', 'foundation', 'grant', 'funding', 
        'team', 'organization', 'decision', 'process', 'structure'
    },
    
    'media_philosophy': {
        'culture', 'philosophy', 'values', 'vision', 'mission', 'ethos', 
        'decentralization', 'freedom', 'innovation', 'future', 'principles'
    },
    
    'announcements': {
        'announcement', 'news', 'press', 'release', 'statement', 'official', 
        'communication', 'update', 'information', 'notification'
    }
}
