import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CategorizeComponent } from './categorize.component';

describe('CategorizeComponent', () => {
  let component: CategorizeComponent;
  let fixture: ComponentFixture<CategorizeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CategorizeComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CategorizeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
