#!/bin/bash

# TEST SCRIPT - All 3 Improvements
# Run this after setting PROXYCURL_API_KEY

set -e

echo "======================================"
echo "🚀 TESTING KUCIBOK V1.2 IMPROVEMENTS"
echo "======================================"
echo ""

# Check API key
if [ -z "$PROXYCURL_API_KEY" ]; then
    echo "❌ ERROR: PROXYCURL_API_KEY not set"
    echo "   Run: export PROXYCURL_API_KEY=pk_your_key"
    exit 1
fi

echo "✅ API Key configured: ${PROXYCURL_API_KEY:0:5}..."
echo ""

# Test 1: Health Check
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
HEALTH=$(curl -s http://localhost:8000/api/monitoring/health)
if echo "$HEALTH" | grep -q "ok"; then
    echo "✅ API is healthy"
else
    echo "❌ API not responding"
    exit 1
fi
echo ""

# Test 2: LinkedIn Curator Monitoring
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  LinkedIn Curator Monitoring"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Triggering LinkedIn monitoring job..."
LINKEDIN_RESULT=$(curl -s -X POST http://localhost:8000/api/monitoring/jobs/monitor-linkedin)
TASK_ID=$(echo "$LINKEDIN_RESULT" | grep -o '"task_id":"[^"]*"' | cut -d'"' -f4)
echo "✅ Job queued: $TASK_ID"
sleep 3
echo ""

# Test 3: Instagram Artist Analysis
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  Instagram Artist Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Triggering Instagram analysis job..."
INSTAGRAM_RESULT=$(curl -s -X POST http://localhost:8000/api/monitoring/jobs/analyze-instagram)
TASK_ID=$(echo "$INSTAGRAM_RESULT" | grep -o '"task_id":"[^"]*"' | cut -d'"' -f4)
echo "✅ Job queued: $TASK_ID"
sleep 3
echo ""

# Test 4: Advanced Artist Re-scoring
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  Advanced Artist Re-scoring"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Triggering artist re-scoring job..."
SCORING_RESULT=$(curl -s -X POST http://localhost:8000/api/monitoring/jobs/rescore-artists-advanced)
TASK_ID=$(echo "$SCORING_RESULT" | grep -o '"task_id":"[^"]*"' | cut -d'"' -f4)
echo "✅ Job queued: $TASK_ID"
sleep 3
echo ""

# Test 5: View Recent Signals
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5️⃣  Recent Signals (if any)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SIGNALS=$(curl -s "http://localhost:8000/api/monitoring/signals/recent?limit=5&days=7")
SIGNAL_COUNT=$(echo "$SIGNALS" | grep -o '"total":[0-9]*' | cut -d':' -f2)
echo "📊 Signals detected: $SIGNAL_COUNT"
echo ""

# Test 6: Dashboard Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6️⃣  Dashboard Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SUMMARY=$(curl -s http://localhost:8000/api/monitoring/summary)
echo "$SUMMARY" | jq '.' 2>/dev/null || echo "$SUMMARY"
echo ""

# Test 7: Job Status
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7️⃣  Job Status (Running/Completed)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
JOBS=$(curl -s "http://localhost:8000/api/monitoring/jobs?limit=10")
echo "$JOBS" | jq '.items[] | {job_type, status, result_count}' 2>/dev/null | head -20
echo ""

echo "======================================"
echo "✅ ALL TESTS COMPLETE!"
echo "======================================"
echo ""
echo "📊 Next Steps:"
echo "1. Open Dashboard: http://localhost:3000"
echo "2. Check logs: docker-compose logs -f app"
echo "3. Wait for jobs to complete (5-10 min)"
echo "4. Verify signals appear in API"
echo ""
echo "📚 Documentation:"
echo "- IMPROVEMENTS_COMPLETE_GUIDE.md"
echo "- LINKEDIN_INSTAGRAM_SETUP.md"
echo ""
