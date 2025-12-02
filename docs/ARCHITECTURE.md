# System Architecture

## Overview

Arc Flash Studio is a web-based application for calculating arc flash incident energy according to IEEE 1584-2018 standard. The system uses a modern three-tier architecture with clear separation of concerns.

![System Architecture](diagrams/system-architecture.svg)

## Design Principles

### 1. Separation of Concerns
- **Frontend**: User interaction and visualization only
- **Backend**: Business logic and calculations
- **Data Layer**: Persistence and retrieval

### 2. API-First Design
All functionality is exposed via REST API, enabling:
- Multiple clients (web, mobile, CLI)
- Third-party integrations
- Automated testing

### 3. Standards Compliance
- IEEE 1584-2018 for arc flash calculations
- NFPA 70E for PPE categories
- NEC for equipment ratings

### 4. Extensibility
- Plugin architecture for future standards (IEC, etc.)
- Equipment library contributions
- Custom report templates

## Technology Stack

### Frontend
- **Framework**: React 18+ with Vite
- **Styling**: Tailwind CSS
- **State**: React Context + Hooks (may upgrade to Zustand)
- **HTTP**: Fetch API with error handling
- **Icons**: Lucide React

**Why these choices?**
- React: Industry standard, massive ecosystem
- Vite: Fast development, optimized builds
- Tailwind: Rapid styling without CSS bloat

### Backend
- **Framework**: FastAPI
- **Calculation**: PandaPower + custom IEEE 1584-2018
- **Validation**: Pydantic v2
- **Database**: SQLite (development) → PostgreSQL (production)

**Why these choices?**
- FastAPI: Modern, fast, auto-generates OpenAPI docs
- PandaPower: Industry-standard power system library
- Pydantic: Type safety and validation

### Infrastructure
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **Deployment**: Docker containers
- **Hosting**: (TBD - Vercel frontend, Railway/Render backend)

## Data Flow

### 1. Calculation Request Flow
```
User Input → Frontend Validation → API Request → 
Backend Validation → PandaPower (Short Circuit) → 
IEEE 1584 Engine → Result Validation → 
Response → Frontend Display
```

### 2. Project Save Flow
```
User Action → Frontend → POST /projects → 
Validation → Database Write → 
Confirmation → Frontend Update
```

## Security Considerations

### Input Validation
- All user inputs validated on both frontend and backend
- Pydantic models enforce type safety
- Range checks for physical parameters

### API Security
- Rate limiting (100 requests/minute)
- CORS configuration for production
- Input sanitization

### Data Privacy
- No sensitive data collected
- Projects stored per-user (when auth added)
- Optional anonymous usage

## Performance Requirements

- **API Response Time**: < 500ms for single equipment
- **Calculation Time**: < 2s for 50-equipment system
- **Frontend Load**: < 2s on 3G connection
- **Database Queries**: < 100ms

## Scalability Plan

### Phase 1 (Current): Single-user
- SQLite database
- In-memory calculations
- Local file storage

### Phase 2: Multi-user
- PostgreSQL database
- User authentication
- Cloud file storage (S3)

### Phase 3: Enterprise
- Calculation queue (Celery)
- Caching layer (Redis)
- Load balancing
- Microservices architecture

## Error Handling Strategy

### Frontend
- User-friendly error messages
- Retry logic for transient failures
- Offline capability (future)

### Backend
- Structured error responses
- Detailed logging
- Graceful degradation

## Testing Strategy

### Unit Tests
- Backend: pytest (>80% coverage target)
- Frontend: Vitest + React Testing Library

### Integration Tests
- API endpoint testing
- Database operations
- PandaPower integration

### Validation Tests
- Known calculation test cases
- Comparison with commercial tools
- Edge case handling

## Future Enhancements

1. **Visual Network Builder**: Drag-drop equipment placement
2. **Batch Processing**: Upload CSV, calculate entire facility
3. **Comparison Mode**: Before/after scenarios
4. **Report Templates**: Customizable PDF reports
5. **Equipment Database**: Community-contributed library
6. **Mobile App**: React Native version
7. **API Marketplace**: Third-party integrations

## References

- [IEEE 1584-2018](https://standards.ieee.org/standard/1584-2018.html)
- [NFPA 70E](https://www.nfpa.org/70E)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PandaPower Documentation](https://pandapower.readthedocs.io/)