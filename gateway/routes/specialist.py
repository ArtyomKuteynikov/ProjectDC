import datetime

from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from typing import List

from models.specialist import Specialist, LanguageProficiency, SpecialistSkill, SpecialistIndustry, Language, Skill, \
    Industry, ProfessionalCommunity, DiplomaCertificate, Education, Project, Specialisation
from schemas.specialist import SpecialistCreate, SpecialistReadSchema, SpecialistUpdate, SpecialistSearch, \
    SimpleResponse, SpecialistsResponse, SpecialistResponse, GetSpecialist, SearchSpecialistsResponse
from config.database import get_db

from models.auth import User, RequestForm

from schemas.specialist import LanguageSchema, SkillSchema, IndustrySchema, ProfessionalCommunitySchema, \
    DiplomaCertificateSchema, EducationSchema, ProjectSchema

router = APIRouter(
    prefix="/v1/specialists",
    tags=['Specialists']
)


async def foreach(arr1, arr2, arg):
    ids_array = [value[arg] for value in arr2]
    for value in arr1:
        if value not in ids_array:
            return False
    return True


async def get_languages(specialist_id: int, session: AsyncSession):
    languages = await session.execute(
        select(LanguageProficiency).where(
            (LanguageProficiency.specialist_id == specialist_id)
        )
    )
    languages = languages.all()
    data = []
    for language in languages:
        lang = language[0].__dict__
        lang.pop('_sa_instance_state')
        language = await session.execute(
            select(Language).where(
                (Language.id == lang['language_id'])
            )
        )
        lang.update({'name': language.first()[0].name})
        data.append(lang)
    return data


async def get_skills(specialist_id: int, session: AsyncSession):
    languages = await session.execute(
        select(SpecialistSkill).where(
            (SpecialistSkill.specialist_id == specialist_id)
        )
    )
    languages = languages.all()
    data = []
    for language in languages:
        lang = language[0].__dict__
        lang.pop('_sa_instance_state')
        language = await session.execute(
            select(Skill).where(
                (Skill.id == lang['skill_id'])
            )
        )
        lang.update({'name': language.first()[0].name})
        data.append(lang)
    return data


async def get_industries(specialist_id: int, session: AsyncSession):
    languages = await session.execute(
        select(SpecialistIndustry).where(
            (SpecialistIndustry.specialist_id == specialist_id)
        )
    )
    languages = languages.all()
    data = []
    for language in languages:
        lang = language[0].__dict__
        lang.pop('_sa_instance_state')
        language = await session.execute(
            select(Industry).where(
                (Industry.id == lang['industry_id'])
            )
        )
        lang.update({'name': language.first()[0].name})
        data.append(lang)
    return data


async def get_communities(specialist_id: int, session: AsyncSession):
    communities = await session.execute(
        select(ProfessionalCommunity).where(
            (ProfessionalCommunity.specialist_id == specialist_id)
        )
    )
    communities = communities.all()
    data = []
    for community in communities:
        comm = community[0].__dict__
        comm.pop('_sa_instance_state')
        data.append(comm)
    return data


async def get_diplomas(specialist_id: int, session: AsyncSession):
    communities = await session.execute(
        select(DiplomaCertificate).where(
            (DiplomaCertificate.specialist_id == specialist_id)
        )
    )
    communities = communities.all()
    data = []
    for community in communities:
        comm = community[0].__dict__
        comm.pop('_sa_instance_state')
        data.append(comm)
    return data


async def get_education(specialist_id: int, session: AsyncSession):
    communities = await session.execute(
        select(Education).where(
            (Education.specialist_id == specialist_id)
        )
    )
    communities = communities.all()
    data = []
    for community in communities:
        comm = community[0].__dict__
        comm.pop('_sa_instance_state')
        data.append(comm)
    return data


async def get_projects(specialist_id: int, session: AsyncSession):
    communities = await session.execute(
        select(Project).where(
            (Project.specialist_id == specialist_id)
        )
    )
    communities = communities.all()
    data = []
    experience = datetime.timedelta(days=0)
    for community in communities:
        comm = community[0].__dict__
        experience += comm['end_date'] - comm['start_date']
        comm.pop('_sa_instance_state')
        data.append(comm)
    return data, experience.days / 365


async def get_specialisation(specialisation_id: int, session: AsyncSession):
    communities = await session.execute(
        select(Specialisation).where(
            (Specialisation.id == specialisation_id)
        )
    )
    communities = communities.first()
    comm = communities[0].__dict__
    comm.pop('_sa_instance_state')
    return comm


async def get_specialisation_by_slug(specialisation: str, session: AsyncSession):
    print(specialisation)
    communities = await session.execute(
        select(Specialisation).where(
            (Specialisation.slug == specialisation)
        )
    )
    communities = communities.first()
    comm = communities[0].__dict__
    comm.pop('_sa_instance_state')
    return comm


async def specialist_availability(specialist_id: int, session: AsyncSession):
    communities = await session.execute(
        select(RequestForm).where(
            (RequestForm.specialist_id == specialist_id) & (RequestForm.status == "work")
        )
    )
    requests = sorted(communities.all(), key=lambda x: x[0].to_date)
    if not requests:
        return datetime.datetime.now(), True
    return requests[-1][0].to_date + datetime.timedelta(days=1), False


async def specialist2dict(specialist_id: int, session: AsyncSession):
    specialist = await session.execute(
        select(Specialist).where(
            (Specialist.id == specialist_id)
        )
    )
    specialist = specialist.first()
    d = specialist[0].__dict__
    d.pop('_sa_instance_state')
    if "password" in d:
        d.pop('password')
    data = await get_languages(d['id'], session)
    d.update({'language': data})
    data = await get_skills(d['id'], session)
    d.update({'skill': data})
    data = await get_industries(d['id'], session)
    d.update({'indusrty': data})
    data = await get_communities(d['id'], session)
    d.update({'community': data})
    data = await get_diplomas(d['id'], session)
    d.update({'diplomas': data})
    data = await get_education(d['id'], session)
    d.update({'education': data})
    data, experience = await get_projects(d['id'], session)
    d.update({'project': data})
    d.update({'experience': experience})
    data = await get_specialisation(d['specialisation_id'], session)
    d.update({'specialisation': data})
    available_date, available_now = await specialist_availability(d['id'], session)
    d.update({'availability_date': available_date.strftime('%d.%m.%Y')})
    d.update({'available_now': available_now})
    return d


@router.get('/', response_model=SpecialistsResponse)
async def read_all_specialists(session: AsyncSession = Depends(get_db)):
    specialist = await session.execute(
        select(Specialist)
    )
    specialist = specialist.all()
    return {
        'specialists': [await specialist2dict(i[0].id, session) for i in specialist],
        'total': len(specialist)
    }


@router.get('/my/', response_model=SpecialistsResponse)
async def read_my_specialists(Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where((User.id == current_user))
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where((Specialist.company_id == user[0].company_id))
    )
    specialist = specialist.all()
    return {
        'specialists': [await specialist2dict(i[0].id, session) for i in specialist],
        'total': len(specialist)
    }


@router.get('/{specialist_id}', response_model=GetSpecialist)
async def read_specialist(specialist_id: int, session: AsyncSession = Depends(get_db)):
    specialist = await session.execute(
        select(Specialist).where(
            (Specialist.id == specialist_id)
        )
    )
    specialist = specialist.first()
    return {
        'specialist': await specialist2dict(specialist[0].id, session)
    }


@router.post("/language/{specialist_id}", response_model=SimpleResponse)
async def add_language(specialist_id: int, language: LanguageSchema, Authorize: AuthJWT = Depends(),
                       session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where((User.id == current_user))
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(
            (Specialist.id == specialist_id)
        )
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    language_ = LanguageProficiency(
        specialist_id=specialist_id,
        language_id=language.language,
        proficiency_level=language.level
    )
    session.add(language_)
    await session.commit()
    return {'result': True}


@router.delete("/language/{specialist_id}/{language}", response_model=SimpleResponse)
async def delete_language(specialist_id: int, language: int, Authorize: AuthJWT = Depends(),
                          session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where((User.id == current_user))
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(
            (Specialist.id == specialist_id)
        )
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    await session.execute(
        delete(LanguageProficiency).where((LanguageProficiency.id == language))
    )
    await session.commit()
    return {'result': True}


@router.post("/skill/{specialist_id}", response_model=SimpleResponse)
async def add_skill(specialist_id: int, skill: SkillSchema, Authorize: AuthJWT = Depends(),
                    session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    skill_ = SpecialistSkill(
        specialist_id=specialist_id,
        skill_id=skill.skill
    )
    session.add(skill_)
    await session.commit()
    return {'result': True}


@router.delete("/skill/{specialist_id}/{skill_id}", response_model=SimpleResponse)
async def delete_skill(specialist_id: int, skill_id: int, Authorize: AuthJWT = Depends(),
                       session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    await session.execute(
        delete(SpecialistSkill).where(SpecialistSkill.id == skill_id)
    )
    await session.commit()
    return {'result': True}


@router.post("/industry/{specialist_id}", response_model=SimpleResponse)
async def add_industry(specialist_id: int, industry: IndustrySchema, Authorize: AuthJWT = Depends(),
                       session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    industry_ = SpecialistIndustry(
        specialist_id=specialist_id,
        industry_id=industry.industry
    )
    session.add(industry_)
    await session.commit()
    return {'result': True}


@router.delete("/industry/{specialist_id}/{industry_id}", response_model=SimpleResponse)
async def delete_industry(specialist_id: int, industry_id: int, Authorize: AuthJWT = Depends(),
                          session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    await session.execute(
        delete(SpecialistIndustry).where(SpecialistIndustry.id == industry_id)
    )
    await session.commit()
    return {'result': True}


@router.post("/professional-community/{specialist_id}", response_model=SimpleResponse)
async def create_professional_community(specialist_id: int, community_data: ProfessionalCommunitySchema,
                                        Authorize: AuthJWT = Depends(),
                                        session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    community = ProfessionalCommunity(**community_data.dict(), specialist_id=specialist_id)
    session.add(community)
    await session.commit()
    return {"result": True}


@router.put("/professional-community/{community_id}", response_model=SimpleResponse)
async def update_professional_community(community_id: int, community_data: ProfessionalCommunitySchema,
                                        Authorize: AuthJWT = Depends(),
                                        session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(ProfessionalCommunity, community_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    for key, value in community_data.dict().items():
        setattr(community, key, value) if value is not None else None
    await session.commit()
    return {'result': True}


@router.delete("/professional-community/{community_id}", response_model=SimpleResponse)
async def delete_professional_community(community_id: int, Authorize: AuthJWT = Depends(),
                                        session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(ProfessionalCommunity, community_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    await session.delete(community)
    await session.commit()
    return {'result': True}


@router.post("/diploma/{specialist_id}", response_model=SimpleResponse)
async def create_diploma(specialist_id: int, community_data: DiplomaCertificateSchema,
                         Authorize: AuthJWT = Depends(),
                         session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    community = DiplomaCertificate(**community_data.dict(), specialist_id=specialist_id)
    session.add(community)
    await session.commit()
    return {"result": True}


@router.put("/diploma/{diploma_id}", response_model=SimpleResponse)
async def update_diploma(diploma_id: int, community_data: DiplomaCertificateSchema,
                         Authorize: AuthJWT = Depends(),
                         session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(DiplomaCertificate, diploma_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    for key, value in community_data.dict().items():
        setattr(community, key, value) if value is not None else None
    await session.commit()
    return {'result': True}


@router.delete("/diploma/{diploma_id}", response_model=SimpleResponse)
async def delete_diploma(diploma_id: int, Authorize: AuthJWT = Depends(),
                         session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(DiplomaCertificate, diploma_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    await session.delete(community)
    await session.commit()
    return {'result': True}


@router.post("/education/{specialist_id}", response_model=SimpleResponse)
async def create_education(specialist_id: int, community_data: EducationSchema,
                           Authorize: AuthJWT = Depends(),
                           session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    community = Education(**community_data.dict(), specialist_id=specialist_id)
    session.add(community)
    await session.commit()
    return {"result": True}


@router.put("/education/{education_id}", response_model=SimpleResponse)
async def update_education(education_id: int, community_data: EducationSchema,
                           Authorize: AuthJWT = Depends(),
                           session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(Education, education_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    for key, value in community_data.dict().items():
        setattr(community, key, value) if value is not None else None
    await session.commit()
    return {'result': True}


@router.delete("/education/{education_id}", response_model=SimpleResponse)
async def delete_education(education_id: int, Authorize: AuthJWT = Depends(),
                           session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(Education, education_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    await session.delete(community)
    await session.commit()
    return {'result': True}


@router.post("/project/{specialist_id}", response_model=SimpleResponse)
async def create_project(specialist_id: int, community_data: ProjectSchema,
                         Authorize: AuthJWT = Depends(),
                         session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    community = Project(**community_data.dict(), specialist_id=specialist_id)
    session.add(community)
    await session.commit()
    return {"result": True}


@router.put("/project/{project_id}", response_model=SimpleResponse)
async def update_project(project_id: int, community_data: ProjectSchema,
                         Authorize: AuthJWT = Depends(),
                         session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(Project, project_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    for key, value in community_data.dict().items():
        setattr(community, key, value) if value is not None else None
    await session.commit()
    return {'result': True}


@router.delete("/project/{project_id}", response_model=SimpleResponse)
async def delete_project(project_id: int, Authorize: AuthJWT = Depends(),
                         session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    community = await session.get(Project, project_id)
    if community is None:
        raise HTTPException(status_code=404, detail="Professional Community not found")
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == community[0].specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    await session.delete(community)
    await session.commit()
    return {'result': True}


@router.post('/', response_model=GetSpecialist)
async def create_specialist(specialist: SpecialistCreate, Authorize: AuthJWT = Depends(),
                            session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where((User.id == current_user))
    )
    user = user.fetchone()
    if user[0].status != 1:
        raise HTTPException(
            status_code=403, detail='sign_contract_first'
        )
    if user[0].role != 'partner':
        raise HTTPException(
            status_code=403, detail='incorrect_role'
        )
    specialist_dict = specialist.dict()
    specialist_dict.pop('languages')
    specialist_dict.pop('skills')
    specialist_dict.pop('industries')
    specialist_dict.pop('communities')
    specialist_dict.pop('diplomas')
    specialist_dict.pop('education')
    specialist_dict.pop('projects')
    db_specialist = Specialist(
        **specialist_dict,
        company_id=user[0].company_id
    )
    session.add(db_specialist)
    await session.commit()
    for language in specialist.languages:
        language_ = LanguageProficiency(
            specialist_id=db_specialist.id,
            language_id=language.language,
            proficiency_level=language.level
        )
        session.add(language_)
        await session.commit()
    for skill in specialist.skills:
        skill_ = SpecialistSkill(
            specialist_id=db_specialist.id,
            skill_id=skill
        )
        session.add(skill_)
        await session.commit()
    for industry in specialist.industries:
        industry_ = SpecialistIndustry(
            specialist_id=db_specialist.id,
            industry_id=industry
        )
        session.add(industry_)
        await session.commit()
    for community in specialist.communities:
        community_ = ProfessionalCommunity(
            specialist_id=db_specialist.id,
            name=community.name,
            link=community.name
        )
        session.add(community_)
        await session.commit()
    for certificate in specialist.diplomas:
        certificate_ = DiplomaCertificate(
            specialist_id=db_specialist.id,
            name=certificate.name,
            year_obtained=certificate.year_obtained
        )
        session.add(certificate_)
        await session.commit()
    for certificate in specialist.education:
        certificate_ = Education(
            specialist_id=db_specialist.id,
            level=certificate.level,
            institution=certificate.institution,
            specialty=certificate.specialty,
            start_year=certificate.start_year,
            end_year=certificate.end_year
        )
        session.add(certificate_)
        await session.commit()
    for project in specialist.projects:
        project_ = Project(
            specialist_id=db_specialist.id,
            company_name=project.company_name,
            responsibilities=project.responsibilities,
            start_date=datetime.datetime.strptime(project.start_date, '%Y-%m-%d'),
            end_date=datetime.datetime.strptime(project.end_date, '%Y-%m-%d')
        )
        session.add(project_)
        await session.commit()
    return {
        'specialist': await specialist2dict(db_specialist.id, session)
    }


@router.put("/{specialist_id}", response_model=SimpleResponse)
async def update_specialist(specialist_id: int, specialist_data: SpecialistUpdate,
                            Authorize: AuthJWT = Depends(),
                            session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where(User.id == current_user)
    )
    user = user.fetchone()
    specialist = await session.execute(
        select(Specialist).where(Specialist.id == specialist_id)
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    for key, value in specialist_data.dict().items():
        setattr(specialist, key, value) if value is not None else None
    await session.commit()
    return {"result": True}


@router.delete('/{specialist_id}', response_model=SpecialistsResponse)
async def delete_specialist(specialist_id: int, Authorize: AuthJWT = Depends(),
                            session: AsyncSession = Depends(get_db)):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    user = await session.execute(
        select(User).where((User.id == current_user))
    )
    user = user.fetchone()
    if user[0].role != 'partner':
        raise HTTPException(
            status_code=403, detail='incorrect_role'
        )
    specialist = await session.execute(
        select(Specialist).where(
            (Specialist.id == specialist_id)
        )
    )
    specialist = specialist.first()
    if specialist[0].company_id != user[0].company_id:
        raise HTTPException(status_code=401)
    try:
        await session.execute(
            delete(ProfessionalCommunity).where((ProfessionalCommunity.specialist_id == specialist_id))
        )
        await session.execute(
            delete(LanguageProficiency).where((LanguageProficiency.specialist_id == specialist_id))
        )
        await session.execute(
            delete(DiplomaCertificate).where((DiplomaCertificate.specialist_id == specialist_id))
        )
        await session.execute(
            delete(Education).where((Education.specialist_id == specialist_id))
        )
        await session.execute(
            delete(SpecialistSkill).where((SpecialistSkill.specialist_id == specialist_id))
        )
        await session.execute(
            delete(SpecialistIndustry).where((SpecialistIndustry.specialist_id == specialist_id))
        )
        await session.execute(
            delete(Project).where((Project.specialist_id == specialist_id))
        )
        await session.execute(
            delete(Specialist).where((Specialist.id == specialist_id))
        )
        await session.commit()
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=404, detail='specialist_not_found'
        )
    specialist = await session.execute(
        select(Specialist)
    )
    specialist = specialist.all()
    return {
        'specialists': [await specialist2dict(i[0].id, session) for i in specialist],
        'total': len(specialist)
    }


@router.post('/search', response_model=SearchSpecialistsResponse)
async def search_specialists(search_data: SpecialistSearch, session: AsyncSession = Depends(get_db)):
    query = select(Specialist)
    if search_data.specialisation and search_data.specialisation != 'all':
        spec = await get_specialisation_by_slug(search_data.specialisation, session)
        query = query.filter(Specialist.specialisation_id == spec['id'])
    if search_data.gender is not None and search_data.gender != 'all':
        query = query.filter(Specialist.gender == search_data.gender)
    if search_data.min_age is not None:
        query = query.filter(Specialist.age >= search_data.min_age)
    if search_data.max_age is not None:
        query = query.filter(Specialist.age <= search_data.max_age)
    if search_data.min_rate is not None:
        query = query.filter(Specialist.hourly_rate >= search_data.min_rate)
    if search_data.max_rate is not None:
        query = query.filter(Specialist.hourly_rate <= search_data.max_rate)
    if search_data.country is not None and search_data.country != 'all':
        query = query.filter(Specialist.country == search_data.country)
    """if search_data.city is not None and search_data.city != 'all':
        query = query.filter(Specialist.city == search_data.city)"""
    if search_data.grade is not None and search_data.grade != 'all':
        query = query.filter(Specialist.grade == search_data.grade)
    if search_data.work_format is not None and search_data.work_format != 'all':
        query = query.filter(Specialist.work_format == search_data.work_format)
    if search_data.international_projects_ready is not None and search_data.international_projects_ready != 'all':
        query = query.filter(Specialist.international_projects_ready == search_data.international_projects_ready)
    specialists = await session.execute(query.order_by(text(search_data.sort.split('#')[0])))
    specialists = specialists.all()[::-1] if search_data.sort.split('#')[1] == 'down' else specialists.all()
    specialists_filtered = []
    for specialist in specialists:
        _, experience = await get_projects(specialist[0].id, session)
        availability_data = await specialist_availability(specialist[0].id, session)
        if search_data.min_work_experience:
            if experience > search_data.min_work_experience:
                continue
        if search_data.city:
            if specialist[0].city not in search_data.city:
                continue
        if search_data.min_work_experience:
            if experience > search_data.max_work_experience:
                continue
        if search_data.availability_date:
            if availability_data[0].date() > datetime.datetime.strptime(search_data.availability_date,
                                                                        '%Y-%m-%d').date():
                continue
        if search_data.languages:
            data = await get_languages(specialist[0].id, session)
            if not await foreach(search_data.languages, data, 'language_id'):
                continue
        if search_data.skills:
            data = await get_skills(specialist[0].id, session)
            if not await foreach(search_data.skills, data, 'skill_id'):
                continue
        if search_data.industries:
            data = await get_industries(specialist[0].id, session)
            if not await foreach(search_data.industries, data, 'industry_id'):
                continue
        specialists_filtered.append(specialist)
    return {
        'specialists': [await specialist2dict(i[0].id, session) for i in specialists_filtered][
                       search_data.limit * (search_data.page - 1): search_data.limit * search_data.page],
        'result': True,
        'page': search_data.page,
        'total': len(specialists_filtered)
    }
